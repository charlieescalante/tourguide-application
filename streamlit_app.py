import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="History Tour", layout="centered", page_icon="🗺️")

# --- CSS Styles ---
st.markdown("""
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

.loading {
    text-align: center;
    margin: 20px 0;
}

.guide-text {
    margin-top: 30px;
    font-size: 1.2em;
    line-height: 1.6em;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Variables ---
if "coords" not in st.session_state:
    st.session_state.coords = None
if "guide_text" not in st.session_state:
    st.session_state.guide_text = None
if "error" not in st.session_state:
    st.session_state.error = None
if "fetching_location" not in st.session_state:
    st.session_state.fetching_location = True
if "fetching_guide" not in st.session_state:
    st.session_state.fetching_guide = False

# --- Title ---
st.markdown('<div class="title">History Tour</div>', unsafe_allow_html=True)

# Instructions to get location
st.markdown("**Note:** Please allow location access in your browser. Once granted, click 'Get Current Location' to proceed.")
get_location_btn = st.button("Get Current Location")

# For demonstration, we mock the coordinates after the user clicks the button.
# In a real scenario, you would use a streamlit-geolocation component or similar.
if get_location_btn:
    # Example coordinates (Statue of Liberty)
    mock_lat, mock_lon = 40.689247, -74.044502
    st.session_state.coords = (mock_lat, mock_lon)
    st.session_state.fetching_location = False

# Check if we got coords or not
if st.session_state.fetching_location:
    st.info("Awaiting location permissions and retrieval...")
elif st.session_state.coords is None:
    st.session_state.error = "Unable to fetch GPS coordinates. Please check permissions."

# If we have coordinates, fetch the guided tour
if st.session_state.coords and st.session_state.guide_text is None and not st.session_state.fetching_guide:
    st.session_state.fetching_guide = True
    st.info("Fetching guided tour from server...")

    lat, lon = st.session_state.coords

    # Prepare OpenAI API call
    openai_api_key = st.secrets["openai"]["api_key"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    prompt = f"You are a historical tour guide. Provide a rich, detailed historical tour for the location at latitude {lat}, longitude {lon}. Explain the historical significance of this place and the surrounding area."

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            json_resp = response.json()
            guide_text = json_resp["choices"][0]["message"]["content"]
            st.session_state.guide_text = guide_text.strip()
        else:
            st.session_state.error = "Failed to connect to the server."
    except Exception as e:
        st.session_state.error = f"Error: {str(e)}"

    st.session_state.fetching_guide = False

# Display guide or error
if st.session_state.error:
    st.markdown(f'<div class="error-text">{st.session_state.error}</div>', unsafe_allow_html=True)
elif st.session_state.fetching_guide:
    st.info("Retrieving the guided tour content...")
elif st.session_state.guide_text:
    # Show the guided tour text
    st.markdown(f'<div class="guide-text">{st.session_state.guide_text}</div>', unsafe_allow_html=True)

    # Add TTS functionality using the browser's Web Speech API
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

    # Buttons to control TTS
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    play_col, pause_col = st.columns([1,1], gap="medium")
    with play_col:
        if st.button("Play", key="play_button"):
            st.markdown("<script>playSpeech();</script>", unsafe_allow_html=True)
    with pause_col:
        if st.button("Pause", key="pause_button"):
            st.markdown("<script>pauseSpeech();</script>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
