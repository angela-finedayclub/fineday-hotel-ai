# api/chat.py
import json
import os

# 將 from openai import OpenAI 移到函式內部，確保環境問題不會在頂層崩潰
# 這裡先保留 import，但我們將在內部加強保護

def handler(request):
    try:
        # **關鍵步驟：這裡必須是您 Vercel 部署的版本**
        # 由於您在 Vercel Log 中已經看到了 500 錯誤，程式碼應該已經被執行到了這裡。
        # 再次確保您的程式碼沒有任何額外頂層代碼。

        from openai import OpenAI
        
        # 安全地獲取 API Key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
             return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Configuration Error: OPENAI_API_KEY not set."})
            }
        
        # 僅在這裡進行客戶端初始化
        client = OpenAI(api_key=api_key)
        
        # 獲取請求數據 (Vercel 處理的請求物件)
        body = json.loads(request.get_data())
        user_message = body.get("message", "")

        # ... (以下邏輯不變)
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

        # 回傳 Vercel 格式
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"reply": reply})
        }

    except ImportError as e:
        # 專門捕獲套件安裝/導入錯誤
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Import Error (Missing Package?): {str(e)}"})
        }

    except Exception as e:
        # 捕獲所有其他執行時錯誤
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Internal Runtime Error: {str(e)}"})
        }