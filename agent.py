from enum import Enum
from config import MAX_RETRIES
from api_client import lookup_account, process_payment
from llm_service import extract_entities
from validators import is_valid_date, validate_payment

class State(Enum):
    AWAITING_ACCOUNT_ID = 1
    AWAITING_VERIFICATION = 2
    AWAITING_PAYMENT = 3
    COMPLETED = 4
    FAILED = 5

class Agent:
    def __init__(self):
        self.state = State.AWAITING_ACCOUNT_ID
        self.retries = 0
        self.account_data = {}
        self.memory = {}

    def next(self, user_input: str) -> dict:
        if self.state in [State.COMPLETED, State.FAILED]:
            return {"message": "This session has ended. Please start a new conversation."}

        extracted = extract_entities(user_input)
        for key, value in extracted.items():
            if value is not None:
                self.memory[key] = value

        try:
            if self.state == State.AWAITING_ACCOUNT_ID:
                return {"message": self._handle_account()}
            elif self.state == State.AWAITING_VERIFICATION:
                return {"message": self._handle_verification()}
            elif self.state == State.AWAITING_PAYMENT:
                return {"message": self._handle_payment()}
        except Exception as e:
            return {"message": f"System encountered an unexpected error: {str(e)}"}

        return {"message": "State evaluation error."}

    def _handle_account(self) -> str:
        account_id = self.memory.get("account_id")
        if not account_id:
            return "Hello! Please share your account ID to get started."

        status, data = lookup_account(account_id)
        
        if status == 200:
            self.account_data = data
            self.state = State.AWAITING_VERIFICATION
            return self._handle_verification()
        if status == 404:
            self.memory.pop("account_id", None)
            return "No account found with that ID. Please check and provide it again."
            
        return "System error connecting to the account database. Please try again later."

    def _handle_verification(self) -> str:
        name = self.memory.get("full_name")
        dob = self.memory.get("dob")
        aadhaar = self.memory.get("aadhaar_last4")
        pincode = self.memory.get("pincode")

        if not name:
            return "Got it. Could you please confirm your full name?"
        if not any([dob, aadhaar, pincode]):
            return "Please verify your identity by providing your date of birth (YYYY-MM-DD), Aadhaar last 4 digits, or pincode."

        if dob and not is_valid_date(dob):
            self.memory.pop("dob", None)
            return "The date of birth provided is not a valid calendar date. Please use YYYY-MM-DD format."

        name_match = (name == self.account_data.get("full_name"))
        sec_match = False
        
        if dob and dob == self.account_data.get("dob"):
            sec_match = True
        elif aadhaar and str(aadhaar) == str(self.account_data.get("aadhaar_last4")):
            sec_match = True
        elif pincode and str(pincode) == str(self.account_data.get("pincode")):
            sec_match = True

        if name_match and sec_match:
            self.state = State.AWAITING_PAYMENT
            self.retries = 0
            balance = self.account_data.get('balance', 0)
            return f"Identity verified. Your outstanding balance is ₹{balance}. Please provide your card number, CVV, expiry month/year, name on card, and payment amount."
        
        self.retries += 1
        if self.retries >= MAX_RETRIES:
            self.state = State.FAILED
            return "Verification failed too many times. Session closed."
        
        for key in ["full_name", "dob", "aadhaar_last4", "pincode"]:
            self.memory.pop(key, None)
            
        return f"Information does not match our records. Please try again. (Attempt {self.retries}/{MAX_RETRIES})"

    def _handle_payment(self) -> str:
        required = ["card_number", "cvv", "expiry_month", "expiry_year", "cardholder_name", "amount"]
        missing = [f.replace("_", " ").title() for f in required if not self.memory.get(f)]
        if missing:
            return f"Please provide the missing details: {', '.join(missing)}."

        val_err = validate_payment(self.memory, self.account_data.get("balance", 0))
        if val_err:
            if "amount" in val_err.lower():
                self.memory.pop("amount", None)
            else:
                for k in ["card_number", "cvv", "expiry_month", "expiry_year"]:
                    self.memory.pop(k, None)
            return val_err

        payload = {
            "account_id": self.account_data["account_id"],
            "amount": float(self.memory["amount"]),
            "payment_method": {
                "type": "card",
                "card": {
                    "cardholder_name": self.memory["cardholder_name"],
                    "card_number": str(self.memory["card_number"]).replace(" ", "").replace("-", ""),
                    "cvv": str(self.memory["cvv"]),
                    "expiry_month": int(self.memory["expiry_month"]),
                    "expiry_year": int(self.memory["expiry_year"])
                }
            }
        }
        
        status, data = process_payment(payload)
        
        for key in ["card_number", "cvv", "expiry_month", "expiry_year"]:
            self.memory.pop(key, None)

        if status == 200:
            self.state = State.COMPLETED
            return f"Payment successful! Your transaction ID is {data.get('transaction_id', 'Unknown')}. Have a great day!"
            
        if status == 422:
            err = data.get("error_code")
            if err == "insufficient_balance":
                self.state = State.FAILED
                return "Terminal Failure: Payment exceeds outstanding balance. Session closed."
            return "Payment failed with the processor. Please check your details and try again."
            
        return "An unexpected server error occurred during payment processing."