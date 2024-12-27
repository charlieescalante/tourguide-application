import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import requests

# Page Configuration
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🗺️")

st.markdown('<h1 style="text-align: center;">History Tour</h1>', unsafe_allow_html=True)

# Geolocation Button
location = streamlit_geolocation()

# Display location or error
if location:
    if "latitude" in location and "longitude" in location:
        latitude = location["latitude"]
        longitude = location["longitude"]
        st.success(f"Your location: Latitude: {latitude}, Longitude: {longitude}")
        
        # Call OpenAI API to get a guided tour
        if "guide_text" not in st.session_state:
            st.info("Fetching guided tour from OpenAI...")

            # Retrieve the OpenAI API key from secrets
            openai_api_key = st.secrets["openai"]["api_key"]

            # Prepare the headers and prompt for the OpenAI API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            }

            prompt = (
                f"You are a historical tour guide. Provide a rich, detailed historical tour for "
                f"the location at latitude {latitude}, longitude {longitude}. "
                f"Explain the historical significance of this place and the surrounding area."
            )

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 400,
                "temperature": 0.
