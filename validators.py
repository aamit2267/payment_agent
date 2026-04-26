import datetime

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def luhn_check(card_number: str) -> bool:
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def validate_payment(memory: dict, balance: float) -> str | None:
    amount = float(memory["amount"])
    if amount <= 0:
        return "Invalid amount. Payment must be greater than zero."
    if amount > balance:
        return f"Amount exceeds your outstanding balance of ₹{balance}. Please enter a valid amount."

    card = str(memory["card_number"]).replace(" ", "").replace("-", "")
    if not card.isdigit() or not (12 <= len(card) <= 16):
        return "Invalid card length or characters."
    if not luhn_check(card):
        return "The card number is invalid. Please try again."

    cvv = str(memory["cvv"])
    if not cvv.isdigit() or len(cvv) not in [3, 4]:
        return "CVV must be 3 or 4 digits."

    try:
        m = int(memory["expiry_month"])
        y = int(memory["expiry_year"])
        if not (1 <= m <= 12):
            return "Invalid expiry month."
        if y < 2024:
            return "Card is expired."
    except ValueError:
        return "Invalid expiry date format."

    return None