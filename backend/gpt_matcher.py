import openai, json, os
openai.api_key = os.getenv("OPENAI_API_KEY","")

def match_hotel_name(input_name, results):
    if not openai.api_key:
        # 沒 key 時直接回傳原始資料
        return results, "ezTravel", results[0]["price"] if results else "N/A"

    prompt = f"請根據以下 ezTravel 搜尋結果，找出與「{input_name}」最相似的飯店名稱，整理成 JSON：" \
             f"飯店名稱、房型、價格、是否含稅、是否可取消、連結，並指出最低價平台。\n{results}"
    r = openai.ChatCompletion.create(model="gpt-4-turbo",
        messages=[{"role":"user","content":prompt}])
    try:
        data = json.loads(r.choices[0].message.content)
        return data["results"], data["lowest_site"], data["lowest_price"]
    except Exception:
        return results, "ezTravel", results[0]["price"] if results else "N/A"
