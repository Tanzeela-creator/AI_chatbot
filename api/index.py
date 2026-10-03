from http.server import BaseHTTPRequestHandler
import json
import os
from groq import Groq


SYSTEM_PROMPT = """
You are a helpful, friendly, and professional AI assistant.

Your role is to:
- Give clear and accurate answers.
- Explain technical topics in simple language when needed.
- Be polite and respectful.
- If you are unsure about something, clearly say so instead of making up information.
- Keep responses relevant to the user's question.
"""


class handler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )

    def do_POST(self):
        try:
            # Read request body
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Get user message
            user_message = data.get("message", "").strip()

            # Validate input
            if not user_message:
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
            client = Groq(api_key=api_key)

            # Send request to Groq
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            # Get AI response
            bot_response = response.choices[0].message.content

            # Send successful response
            self.send_json(
                200,
                {"response": bot_response}
            )

        except json.JSONDecodeError:
            self.send_json(
                400,
                {"error": "Invalid request format."}
            )

        except Exception as e:
            print("Server error:", str(e))

            self.send_json(
                500,
                {"error": "Something went wrong while processing your request."}
            )