import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def extract_entities(user_text: str) -> dict:
    prompt = f"""
    Extract payment and identity details from the user text exactly as they appear. 
    You must output ONLY a valid JSON object. Use exactly these keys. 
    If a value is missing, use null.
    Keys: "account_id", "full_name", "dob", "aadhaar_last4", "pincode", "card_number", "cvv", "expiry_month", "expiry_year", "cardholder_name", "amount"
    User text: '{user_text}'
    """
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        keys = ["account_id", "full_name", "dob", "aadhaar_last4", "pincode", "card_number", "cvv", "expiry_month", "expiry_year", "cardholder_name", "amount"]
        return {k: None for k in keys}