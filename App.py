from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("================================")
print("       AI CHATBOT")
print("================================")
print("Type 'exit' to close the chatbot.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        print("Chatbot:", response.choices[0].message.content)
        print()

    except Exception as e:
        print("Error:", e)