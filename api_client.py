import requests
from config import API_BASE_URL

def lookup_account(account_id: str) -> tuple[int, dict]:
    url = f"{API_BASE_URL}/lookup-account"
    response = requests.post(url, json={"account_id": account_id})
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, {}

def process_payment(payload: dict) -> tuple[int, dict]:
    url = f"{API_BASE_URL}/process-payment"
    response = requests.post(url, json=payload)
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, {}