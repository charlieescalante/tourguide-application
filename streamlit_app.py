import streamlit as st
import requests
from streamlit_geolocation import geolocation

# 1. Page Configuration
st.set_page_config(
    page_title="History Tour",
    layout="centered",
    page_icon="🗺️"
)

# 2. CSS Styles (Optional)
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 2em;
        margin-bottom: 20px;
    }
    .button-row {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .error-text {
        color: red;
        text-align: center;
        margin-top: 20px;
    }
    .guide-text {
        margin-top: 30px;
        font-size: 1.2em;
        line-height: 1.6em;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Title
st.markdown('<div class="title">History Tour</div>', unsafe_allow_html=True)

# 4. Ask the user for permission to access their location
st.info("Please allow location access in your browser when prompted.")
loc_data = geolocation()

# 5. If location data is available, extract the coordinates
if loc_data:
    # 'loc_data' should look something like:
    # {
    #   "coords": {
    #       "latitude": 37.4219983,
    #       "longitude": -122.084,
    #       "accuracy": ...
    #   }
    # }
    latitude = loc_data["coords"]["latitude"]
    longitude = loc_data["coords"]["longitude"]

    # Display the user's real coordinates
    st.write(f"**Your coordinates**: {latitude}, {longitude}")

    # 6. Once we have coords, call OpenAI if we haven't already
    if "guide_text" not in st.session_state:
        # Provide a loading message
        st.info("Fetching guided tour from OpenAI...")

        # Retrieve the API key from Streamlit secrets
        openai_api_key = st.secrets["openai"]["api_key"]

        # Headers for the OpenAI request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        # Create a descriptive prompt for GPT
        prompt = (
            f"You are a historical tour guide. Provide a rich, detailed historical tour for "
            f"the location at latitude {latitude}, longitude {longitude}. "
            f"Explain the historical significance of this place and the surrounding area."
        )

        # The body of the request to the GPT-3.5-turbo endpoint
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 400,
            "temperature": 0.7
        }

        # 7. Make the request to OpenAI
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            # Debugging info (optional, remove or comment out in production)
            st.write("Status code:", response.status_code)
            st.write("Response text:", response.text)

            if response.status_code == 200:
                json_resp = response.json()
                guide_text = json_resp["choices"][0]["message"]["content"]
                st.session_state.guide_text = guide_text.strip()
            else:
                st.session_state.guide_text = "Failed to connect to OpenAI. Please try again later."

        except Exception as e:
            st.session_state.guide_text = f"Error: {str(e)}"

    # 8. If we have a guide text, display it and add TTS
    if "guide_text" in st.session_state and st.session_state.guide_text:
        st.markdown(
            f'<div class="guide-text">{st.session_state.guide_text}</div>',
            unsafe_allow_html=True
        )

        # 9. Text-to-Speech using JavaScript in the browser
        tts_script = f"""
        <script>
        var guideText = `{st.session_state.guide_text.replace('`','\\`')}`;
        var utterance = new SpeechSynthesisUtterance(guideText);
        var synth = window.speechSynthesis;
        var paused = false;
        utterance.rate = 1.0;

        function playSpeech() {{
            if (paused) {{
                synth.resume();
                paused = false;
            }} else {{
                synth.cancel();
                synth.speak(utterance);
            }}
        }}

        function pauseSpeech() {{
            synth.pause();
            paused = true;
        }}
        </script>
        """
        st.markdown(tts_script, unsafe_allow_html=True)

        # TTS control buttons
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        col_play, col_pause = st.columns([1, 1], gap="medium")
        with col_play:
            if st.button("Play", key="play_button"):
                st.markdown("<script>playSpeech();</script>", unsafe_allow_html=True)
        with col_pause:
            if st.button("Pause", key="pause_button"):
                st.markdown("<script>pauseSpeech();</script>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # If location isn't available yet or user denied permission
    st.write("Location data not available yet. Please allow browser location access if prompted.")