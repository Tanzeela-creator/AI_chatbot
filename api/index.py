from http.server import BaseHTTPRequestHandler
import json
import os
from groq import Groq


SYSTEM_PROMPT = """
You are a helpful, friendly, and professional AI assistant.

Identity:
- You are an AI assistant created as part of a chatbot project.
- You are powered by the Groq API.
- Do not claim to be ChatGPT or an OpenAI assistant.

Behavior:
- Give clear and useful answers.
- Explain technical topics in simple language when needed.
- Be polite and respectful.
- Keep responses relevant to the user's question.
- If you are unsure about something, clearly say so instead of making up information.

Response style:
- Use short paragraphs.
- Use bullet points when they make information easier to understand.
- Use Markdown when appropriate.
"""


class handler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )


    def do_OPTIONS(self):

        self.send_json(
            200,
            {"message": "CORS preflight successful"}
        )


    def do_POST(self):

        try:

            # Read request body
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)


            # Get conversation messages
            messages = data.get("messages", [])


            # Validate messages
            if not isinstance(messages, list):

                self.send_json(
                    400,
                    {"error": "Invalid messages format."}
                )

                return


            # Limit conversation history
            messages = messages[-20:]


            # Remove invalid messages
            clean_messages = []

            for message in messages:

                if not isinstance(message, dict):
                    continue

                role = message.get("role")
                content = message.get("content", "")

                if role not in ["user", "assistant"]:
                    continue

                if not isinstance(content, str):
                    continue

                content = content.strip()

                if not content:
                    continue

                clean_messages.append(
                    {
                        "role": role,
                        "content": content
                    }
                )


            # Make sure there is at least one user message
            if not clean_messages:

                self.send_json(
                    400,
                    {"error": "Please enter a message."}
                )

                return


            # Check API key
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:

                self.send_json(
                    500,
                    {"error": "Groq API key is not configured."}
                )

                return


            # Create Groq client
            client = Groq(
                api_key=api_key
            )


            # Add system prompt + conversation history
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            api_messages.extend(
                clean_messages
            )


            # Send request to Groq
            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=api_messages

            )


            # Get AI response
            bot_response = (
                response.choices[0].message.content
            )


            # Send response to frontend
            self.send_json(
                200,
                {
                    "response": bot_response
                }
            )


        except json.JSONDecodeError:

            self.send_json(
                400,
                {
                    "error": "Invalid request format."
                }
            )


        except Exception as e:

            print(
                "Server error:",
                str(e)
            )

            self.send_json(
                500,
                {
                    "error": "Something went wrong while processing your request."
                }
            )