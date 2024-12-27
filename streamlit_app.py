import streamlit as st
import requests
import os

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Set the 'OPENAI_API_KEY' environment variable.")

# Streamlit page setup
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🌍")

if "guide_text" not in st.session_state:
    st.session_state["guide_text"] = ""

st.markdown('<h1 style="text-align: center;">History Tour</h1>', unsafe_allow_html=True)

# Example Geolocation
latitude = 37.7749  # Replace with dynamic geolocation
longitude = -122.4194  # Replace with dynamic geolocation

try:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    prompt = (
        f"You are a historical tour guide. Provide a rich, detailed historical tour for "
        f"the location at latitude {latitude}, longitude {longitude}. "
    )

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 400,
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        json_resp = response.json()
        guide_text = json_resp["choices"][0]["message"]["content"]
        st.session_state["guide_text"] = guide_text.strip()
    else:
        st.error(f"API call failed: {response.status_code} - {response.text}")

except Exception as e:
    st.error(f"Exception occurred: {str(e)}")

st.write(st.session_state["guide_text"])
