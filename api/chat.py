# api/chat.py
import json
import os
from openai import OpenAI

# Vercel Serverless Function 的入口點必須是一個名為 'handler' 或 'app' 的函式
def handler(request):
    try:
        # 安全地獲取 API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Configuration Error: OPENAI_API_KEY not set in Vercel Environment Variables."})
            }
        
        # 延遲初始化 client
        client = OpenAI(api_key=api_key)
        
        # 處理 POST 請求的 JSON 數據
        # Vercel 的 request 物件可以直接獲取 body
        body = json.loads(request.get_data())
        user_message = body.get("message", "")

        if not user_message:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No message provided"})
            }

        # 呼叫 OpenAI API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are FineDay, a warm and professional hotel assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content.strip()

        # 回傳 Vercel 格式的 JSON 響應
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        # 捕捉並回傳所有錯誤細節
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Internal Server Error: {str(e)}"})
        }