# Payment Collection AI Agent

## Project Overview
This project implements an end-to-end payment collection AI agent with strict identity verification and mock API integration. The agent guides users through a secure payment flow:
1. Account ID collection
2. Multi-factor identity verification (name, DOB, Aadhaar last 4, or pincode)
3. Payment processing with card validation and balance checks

The agent uses a state machine to manage the conversation flow, integrates with mock banking APIs for account lookup and payment processing, and leverages an LLM (via Groq) to extract entities from user input.

## File Structure
```
payment_agent/
├── agent.py          # Main state machine orchestrator (State enum and Agent class)
├── api_client.py     # Handles HTTP requests to mock APIs (account lookup and payment processing)
├── validators.py     # Validation logic (date validation, payment validation)
├── llm_service.py    # LLM integration for entity extraction (using Groq API)
├── config.py         # Configuration management (API keys, model, endpoints, constants)
├── run.py            # Interactive CLI entry point for the agent
├── evaluate.py       # Automated evaluation script for testing various scenarios
└── requirements.txt  # Python dependencies
```

### Module Responsibilities
- **agent.py**: Contains the core logic with states (AWAITING_ACCOUNT_ID, AWAITING_VERIFICATION, AWAITING_PAYMENT, COMPLETED, FAILED) and methods to handle each state transition.
- **api_client.py**: Wrapper for POST requests to the mock verification API endpoints.
- **validators.py**: Implements date validation, Luhn algorithm for card numbers, and payment-specific validation (amount, card details, expiry).
- **llm_service.py**: Uses Groq's LLM to extract structured entities from unstructured user text.
- **config.py**: Loads environment variables and sets constants (API base URL, model name, max retries).
- **run.py**: Starts an interactive loop for users to converse with the agent via command line.
- **evaluate.py**: Runs predefined test cases to verify agent behavior (success, failure, edge cases).

## Setup and Installation

1. **Clone the repository** https://github.com/aamit2267/payment_agent.git
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   - Create a `.env` file in the `payment_agent` directory with:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - Obtain a Groq API key from [Groq Cloud](https://console.groq.com/keys).

## How to Run

### Interactive CLI
To start an interactive conversation with the agent:
```bash
python run.py
```
Follow the prompts to provide your account ID, verify your identity, and make a payment.

### Automated Evaluation
To run the test suite that verifies various scenarios:
```bash
python evaluate.py
```
This script tests:
- Successful end-to-end payment
- Verification failure (exhausted retries)
- Payment failure (invalid card/insufficient balance)
- Edge case handling (e.g., invalid date like 2024-02-30)

## Sample Conversations

### 1. Successful End-to-End Payment
```
Agent: Hello! Please share your account ID to get started.
User: ACC1001
Agent: Got it. Could you please confirm your full name?
User: Alice Smith
Agent: Please verify your identity by providing your date of birth (YYYY-MM-DD), Aadhaar last 4 digits, or pincode.
User: My date of birth is 1990-05-15
Agent: Identity verified. Your outstanding balance is ₹5000. Please provide your card number, CVV, expiry month/year, name on card, and payment amount.
User: Card: 4111 1111 1111 1111, CVV: 123, Expiry: 12/25, Name: Alice Smith, Amount: 1000
Agent: Payment successful! Your transaction ID is txn_123456789. Have a great day!
```

### 2. Verification Failure (Exhausted Retries)
```
Agent: Hello! Please share your account ID to get started.
User: ACC1002
Agent: Got it. Could you please confirm your full name?
User: Bob Jones
Agent: Please verify your identity by providing your date of birth (YYYY-MM-DD), Aadhaar last 4 digits, or pincode.
User: My DOB is 1985-08-20
Agent: Information does not match our records. Please try again. (Attempt 1/3)
User: Actually, my DOB is 1985-08-21
Agent: Information does not match our records. Please try again. (Attempt 2/3)
User: Let me try again: 1985-08-22
Agent: Information does not match our records. Please try again. (Attempt 3/3)
Agent: Verification failed too many times. Session closed.
```

### 3. Payment Failure (Invalid Card)
```
Agent: Hello! Please share your account ID to get started.
User: ACC1003
Agent: Got it. Could you please confirm your full name?
User: Carol Lee
Agent: Please verify your identity by providing your date of birth (YYYY-MM-DD), Aadhaar last 4 digits, or pincode.
User: DOB: 1992-11-30
Agent: Identity verified. Your outstanding balance is ₹2000. Please provide your card number, CVV, expiry month/year, name on card, and payment amount.
User: Card: 6011 0000 0000 0004, CVV: 999, Expiry: 10/26, Name: Carol Lee, Amount: 500
Agent: The card number is invalid. Please try again.
User: Card: 4000 0000 0000 0002, CVV: 123, Expiry: 10/26, Name: Carol Lee, Amount: 500
Agent: Payment failed with the processor. Please check your details and try again.
```

### 4. Edge Case Handling (Invalid Date - ACC1004 Leap Year)
```
Agent: Hello! Please share your account ID to get started.
User: ACC1004
Agent: Got it. Could you please confirm your full name?
User: David Brown
Agent: Please verify your identity by providing your date of birth (YYYY-MM-DD), Aadhaar last 4 digits, or pincode.
User: My DOB is 2024-02-30
Agent: The date of birth provided is not a valid calendar date. Please use YYYY-MM-DD format.
User: Oh sorry, 2024-02-29
Agent: Identity verified. Your outstanding balance is ₹1500. Please provide your card number, CVV, expiry month/year, name on card, and payment amount.
User: Card: 5500 0000 0000 0004, CVV: 456, Expiry: 09/27, Name: David Brown, Amount: 300
Agent: Payment successful! Your transaction ID is txn_987654321. Have a great day!
```