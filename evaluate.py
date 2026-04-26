from agent import Agent
import time

def run_scenario(scenario_name: str, user_inputs: list[str]):
    print(f"\n{'='*60}")
    print(f"RUNNING SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    
    agent = Agent()
    
    for user_input in user_inputs:
        print(f"\nUser: {user_input}")
        
        response = agent.next(user_input)
        print(f"Agent: {response['message']}")
        
        if agent.state.name in ["COMPLETED", "FAILED"]:
            print(f"\n>>> Session Terminated with State: {agent.state.name} <<<")
            break
            
        time.sleep(1)

def main():
    scenario_1 = [
        "Hi, I need to make a payment.",
        "My account is ACC1001",
        "My name is Nithin Jain and my pincode is 400001",
        "I will pay 500. Card is 4532015112830366, cvv 123, expiry 12/2027, name Nithin Jain"
    ]

    scenario_2 = [
        "Hello, ACC1002",
        "My name is Raj",
        "Rajarajeswari Balasubramaniam, pincode 999999",
        "Rajarajeswari Balasubramaniam, dob 1980-01-01",
        "Rajarajeswari Balasubramaniam, aadhaar 0000"
    ]

    scenario_3 = [
        "ACC1003",
        "Priya Agarwal, aadhaar 2468",
        "I want to pay 100 rupees. Card 4532015112830366, cvv 123, exp 12/2027, name Priya"
    ]

    scenario_4 = [
        "ACC1004",
        "Rahul Mehta, born on 1989-02-29",
        "Oops, I meant 1988-02-29",
        "Paying 1000. Card is 453201511283036, cvv 12, expiry 13/2020, name Rahul"
    ]

    run_scenario("1. HAPPY PATH (ACC1001 + Out of Order Info)", scenario_1)
    run_scenario("2. VERIFICATION FAILURE (ACC1002 + Max Retries)", scenario_2)
    run_scenario("3. PAYMENT FAILURE (ACC1003 + Insufficient Balance)", scenario_3)
    run_scenario("4. EDGE CASES (ACC1004 + Leap Year + Bad Card Info)", scenario_4)

if __name__ == "__main__":
    main()