import streamlit as st
import openai
import os

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API key not found. Set the 'OPENAI_API_KEY' environment variable.")

# Streamlit page configuration
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🌍")

# Initialize session state for guide text
if "guide_text" not in st.session_state:
    st.session_state["guide_text"] = ""

st.markdown('<h1 style="text-align: center;">History Tour</h1>', unsafe_allow_html=True)

# Example Geolocation
latitude = 37.7749  # Replace with dynamic geolocation
longitude = -122.4194  # Replace with dynamic geolocation

# Function to fetch historical tour information from OpenAI
def get_historical_tour(lat, long):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
                {
                    "role": "user",
                    "content": f"Provide a rich, detailed historical tour for the location at latitude {lat}, longitude {long}."
                },
            ],
            temperature=0.7,
            max_tokens=400,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Generate historical tour when button is clicked
if st.button("Generate Historical Tour"):
    with st.spinner("Fetching historical information..."):
        guide_text = get_historical_tour(latitude, longitude)
        if guide_text:
            st.session_state["guide_text"] = guide_text

# Display the historical tour text
st.write(st.session_state["guide_text"])
