import streamlit as st
import requests
from openai import OpenAI
import os

# ===============================
# 🔒 APIキーの読み込み（Streamlit専用）
# ===============================
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENWEATHER_KEY = st.secrets["OPENWEATHER_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ===============================
# ☁️ 天気情報取得
# ===============================
def get_weather(city="Tokyo"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric&lang=ja"
    res = requests.get(url).json()
    desc = res["weather"][0]["description"]
    temp = res["main"]["temp"]
    return f"{city}の天気は{desc}、気温は{temp}℃です。"

# ===============================
# 👚 AIコーデ提案
# ===============================
def ai_stylist(keyword, city="Tokyo"):
    weather = get_weather(city)
    prompt = f"""
今日の{weather}
キーワード: {keyword}

この条件にぴったりのファッションコーデを提案して。
具体的な服の組み合わせと理由を説明して。
最後にポジティブな一言で締めてください。
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ===============================
# 🎨 画像生成
# ===============================
def generate_image(description):
    image_prompt = f"{description}, おしゃれな全身コーデ, リアルな人物, 明るい背景, 韓国風"
    image = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )
    return image.data[0].url

# ===============================
# 🌟 Streamlit UI
# ===============================
st.title("👗 AIファッションアドバイザー")

keyword = st.text_input("今日の気分・キーワードを入力してね（例：デート、韓国っぽ、カジュアル）")

if st.button("コーデを提案して！"):
    if not keyword:
        st.warning("キーワードを入力してね！")
    else:
        st.write("🧥 **今日のAIコーデ提案**")
        coord_text = ai_stylist(keyword)
        st.write(coord_text)

        st.write("🎨 **参考コーデ画像を生成中…**")
        image_url = generate_image(coord_text)
        st.image(image_url, caption="AI生成コーデ")
