import streamlit as st, requests, pandas as pd

st.set_page_config(page_title="FineDay 飯店查價工具", page_icon="🏨", layout="wide")
st.title("🏨 FineDay 飯店查價工具")
st.markdown("輸入條件後，AI 會自動比對 ezTravel 網站房型與價格。")

with st.form("search_form"):
    city = st.text_input("🌆 城市", "東京")
    hotel = st.text_input("🏨 飯店名稱（可模糊輸入）", "Aman Tokyo")
    c1,c2,c3 = st.columns(3)
    with c1: checkin = st.date_input("📅 入住日期")
    with c2: checkout = st.date_input("📅 退房日期")
    with c3: people = st.number_input("👥 人數", 1, 10, 2)
    submitted = st.form_submit_button("🔍 查詢價格")

if submitted:
    with st.spinner("AI 正在比對 ezTravel 價格中，請稍候..."):
        payload = {
            "city": city, "hotel": hotel,
            "checkin": str(checkin), "checkout": str(checkout), "people": int(people)
        }
        r = requests.post("https://your-backend-url/api/search", json=payload)
        if r.ok:
            data = r.json()
            df = pd.DataFrame(data["results"])
            st.dataframe(df, use_container_width=True)
            st.success(f"💰 最低價平台：{data['lowest_site']}（{data['lowest_price']}）")
        else:
            st.error("查詢失敗，請稍後再試。")
