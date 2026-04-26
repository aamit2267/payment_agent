from agent import Agent

def main():
    print("--- Payment Agent CLI ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    agent = Agent()
    
    response = agent.next("Hi")
    print(f"Agent: {response['message']}")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        response = agent.next(user_input)
        print(f"Agent: {response['message']}")

        if agent.state in ["COMPLETED", "FAILED"]:
            break

if __name__ == "__main__":
    main()