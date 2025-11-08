from openai import OpenAI
import os
from flask import jsonify, request

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handler(request):
    if request.method == "GET":
        return jsonify({"message": "FineDay AI backend is running!"})

    if request.method == "POST":
        try:
            data = request.get_json()
            user_message = data.get("message", "")

            if not user_message:
                return jsonify({"error": "No message provided"}), 400

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are FineDay, a warm and professional hotel assistant."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = completion.choices[0].message.content.strip()
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
