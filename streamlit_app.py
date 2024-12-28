import openai
import os
import streamlit as st

# Load API key from Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]

openai.api_key = openai_api_key

# Streamlit app configuration
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🌍")

if "guide_text" not in st.session_state:
    st.session_state["guide_text"] = ""

st.title("History Tour")

# Example geolocation
latitude = 37.7749  # Replace with dynamic geolocation
longitude = -122.4194  # Replace with dynamic geolocation

try:
    # OpenAI API call using the updated syntax
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
            {"role": "user", "content": f"Provide a rich, detailed historical tour for the location at latitude {latitude}, longitude {longitude}."},
        ],
        temperature=0.7,
        max_tokens=400
    )
    guide_text = response["choices"][0]["message"]["content"]
    st.session_state["guide_text"] = guide_text.strip()
    st.write(st.session_state["guide_text"])

except openai.error.OpenAIError as e:
    st.error(f"OpenAI API call failed: {e}")
