import ollama

MODEL_NAME = "smollm:135m"

def chat_with_model(prompt):
    try:
        print("=> thinking...")
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Chat with Smollm! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chat_with_model(user_input)
        print(f"=> Smollm: {response}")

if __name__ == "__main__":
    main()