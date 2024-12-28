import streamlit as st
import requests
import openai

# Set up OpenAI API key from Streamlit secrets
try:
    openai.api_key = st.secrets["openai"]["api_key"]
except KeyError:
    st.error("OpenAI API key not found in Streamlit secrets. Please check your setup.")
    st.stop()

# Streamlit page setup
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🌍")

# Initialize session state for guide text
if "guide_text" not in st.session_state:
    st.session_state["guide_text"] = ""

# Page title
st.markdown('<h1 style="text-align: center;">History Tour</h1>', unsafe_allow_html=True)

# Example geolocation
latitude = 37.7749  # Replace with dynamic geolocation
longitude = -122.4194  # Replace with dynamic geolocation

# Request to OpenAI API
try:
    prompt = (
        "You are a historical tour guide. Provide a rich, detailed historical tour for "
        f"the location at latitude {latitude}, longitude {longitude}."
    )

    # Request body
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 400,
        "temperature": 0.7,
    }

    # OpenAI API call
    response = openai.ChatCompletion.create(**data)

    # Extract and display response
    guide_text = response["choices"][0]["message"]["content"]
    st.session_state["guide_text"] = guide_text.strip()

except Exception as e:
    st.error(f"OpenAI API call failed: {str(e)}")
    st.stop()

# Display the historical tour content
st.write(st.session_state["guide_text"])
