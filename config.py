import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
API_BASE_URL = "https://se-payment-verification-api.service.external.usea2.aws.prodigaltech.com/api"
MAX_RETRIES = 3