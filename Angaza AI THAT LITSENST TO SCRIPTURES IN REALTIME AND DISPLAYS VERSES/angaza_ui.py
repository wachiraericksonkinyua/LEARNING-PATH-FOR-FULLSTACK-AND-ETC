import streamlit as st
import requests
import os

# Page Config
st.set_page_config(page_title="Angaza", page_icon="🕊️")

st.title("🕊️ Angaza: Faith & Comfort")
st.subheader("How are you feeling today?")

# Sidebar for Language Selection
language = st.sidebar.selectbox("Select Language / Chagua Lugha", ["English", "Swahili"])
lang_code = "en" if language == "English" else "sw"

# User Input
user_feeling = st.text_input("I feel...", placeholder="e.g., anxious about my exams")

if st.button("Get Comfort"):
    if user_feeling:
        with st.spinner("Angaza is reflecting..."):
            # 1. Call your FastAPI Backend
            try:
                # Assuming your endpoint is /scripture/by-emotion
                payload = {"text": user_feeling, "language": lang_code, "user_id": "rome_x230"}
                response = requests.post("http://127.0.0.1:8000/scripture/by-emotion", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 2. Display the Scripture and Devotional
                    st.markdown(f"### 📖 {data['scripture_reference']}")
                    st.write(data['scripture_text'])
                    
                    st.info(data['devotional'])
                    
                    # 3. Handle the Voice Response
                    # If your API returns a base64 audio string:
                    if "audio_base64" in data:
                        import base64
                        audio_bytes = base64.b64decode(data["audio_base64"])
                        st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.error("Could not reach Angaza. Make sure the FastAPI server is running!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please tell me how you feel first.")