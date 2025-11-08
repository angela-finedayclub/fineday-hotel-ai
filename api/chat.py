# api/chat.py (這是 Vercel Serverless Functions 的標準寫法)
import json
import os
from openai import OpenAI

# Vercel 期望在檔案中找到一個名為 'handler' 或 'app' 的可呼叫物件
def handler(request):
    try:
        # 1. 關鍵檢查：延遲/安全初始化
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Configuration Error: OPENAI_API_KEY not set."})
            }
        
        # 只有在函式被呼叫時才初始化 client
        client = OpenAI(api_key=api_key)
        
        # 2. 獲取請求數據
        # Vercel 請求物件處理
        body = json.loads(request.get_data())
        user_message = body.get("message", "")

        if not user_message:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No message provided"})
            }

        # 3. 呼叫 OpenAI API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are FineDay, a warm and professional hotel assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content.strip()

        # 4. 回傳 Vercel 格式
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except Exception as e:
        # 確保任何錯誤都能回傳詳細信息
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Internal Server Error: {str(e)}"})
        }