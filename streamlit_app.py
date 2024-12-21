import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import requests

# Configure the page
st.set_page_config(
    page_title="History Tour",
    layout="centered",
    page_icon="🗺️"
)

# CSS for styling
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 2em;
    margin-bottom: 20px;
}
.guide-text {
    margin-top: 30px;
    font-size: 1.2em;
    line-height: 1.6em;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

# Display the title
st.markdown('<div class="title">History Tour</div>', unsafe_allow_html=True)

# Use streamlit-js-eval to get geolocation
coords = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => resolve(position.coords),
                (error) => reject({ error: error.message })
            );
        } else {
            reject({ error: "Geolocation is not supported by this browser." });
        }
    });
    """
)

# Check if we got coordinates or an error
if coords:
    if "error" in coords:
        st.error(f"Error fetching location: {coords['error']}")
    else:
        latitude = coords["latitude"]
        longitude = coords["longitude"]
        st.success(f"Your coordinates: {latitude}, {longitude}")

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
                "temperature": 0.7
            }

            # Make the POST request to OpenAI
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data
                )

                if response.status_code == 200:
                    json_resp = response.json()
                    guide_text = json_resp["choices"][0]["message"]["content"]
                    st.session_state.guide_text = guide_text.strip()
                else:
                    st.session_state.guide_text = f"Error: {response.status_code} - {response.text}"

            except Exception as e:
                st.session_state.guide_text = f"Exception occurred: {str(e)}"

        # Display the guided tour text
        if "guide_text" in st.session_state and st.session_state.guide_text:
            st.markdown(f'<div class="guide-text">{st.session_state.guide_text}</div>', unsafe_allow_html=True)

else:
    st.warning("Awaiting geolocation permission...")