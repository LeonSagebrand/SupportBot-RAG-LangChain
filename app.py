from chatbot import Chatbot

def main():
    chatbot = Chatbot()

    print("Welcome to the RAG-based Chatbot. Ask your questions:")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot.chat_with_bot(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
