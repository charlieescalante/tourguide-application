import streamlit as st
import requests
import json
import time
from urllib.parse import urlencode

# --- Configuration ---
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

# --- Title ---
st.markdown('<div class="title">History Tour</div>', unsafe_allow_html=True)

# --- State Management ---
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

# --- Geolocation Retrieval ---
# We'll embed JS to request geolocation permissions and send the coords back to Streamlit.
# The trick: We use a simple piece of JS that obtains the location and then redirects 
# the iframe URL with coordinates as query parameters. We can parse them in Python.

location_component = """
<script>
navigator.geolocation.getCurrentPosition(successCallback, errorCallback, {enableHighAccuracy: true});

function successCallback(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    var searchParams = new URLSearchParams(window.location.search);
    searchParams.set('lat', lat);
    searchParams.set('lon', lon);
    window.parent.postMessage({ 'lat': lat, 'lon': lon }, "*");
}

function errorCallback(error) {
    window.parent.postMessage({ 'error': error.message }, "*");
}
</script>
"""

# We'll use a Streamlit component to run this JS. It will send a postMessage to the parent window.
# We can listen to this message in another st.experimental_memo or by using a Streamlit JS callback approach.
# Since Streamlit doesn't directly capture postMessages, we can do a trick by polling a variable set by js.
from streamlit.components.v1 import html

coords_data = html(location_component, height=0, width=0)

# A small workaround: We'll use a communication approach by capturing the message via a hidden element using window.onmessage in HTML and a form submission simulation.
# However, Streamlit doesn't allow direct JS->Python comm easily. Another approach is to check st.session_state.
# In practice, you'd use streamlit-javascript or a similar component. For simplicity, let's just show a button after permission is granted.
# 
# Since we cannot directly capture the postMessage in Streamlit easily, let's provide a small instruction:
st.markdown("**Note:** Please allow location access in your browser. Once granted, click 'Get Current Location' to proceed.")
get_location_btn = st.button("Get Current Location")

if get_location_btn:
    # Attempt to use geopy or a placeholder since we cannot truly capture from JS directly in this environment.
    # In a real deployment, you'd handle the JS -> Python communication via a custom Streamlit component.
    # For demonstration, let's simulate location retrieval failure or success.
    # (In a real scenario, you'd implement a custom component or use `streamlit-javascript` to get coords.)
    
    # We'll assume the user grants permission and we can mock coordinates here.
    # Replace this with actual logic if using a custom component that returns lat/lon.
    # For demonstration:
    mock_lat, mock_lon = 40.689247, -74.044502  # Coordinates near Statue of Liberty, as example.
    st.session_state.coords = (mock_lat, mock_lon)
    st.session_state.fetching_location = False

# If coords still None, show a spinner or error
if st.session_state.fetching_location:
    st.info("Awaiting location permissions and retrieval...")
elif st.session_state.coords is None:
    # If we have no coords after user click, show error
    st.session_state.error = "Unable to fetch GPS coordinates. Please check permissions."
else:
    # We have coords
    pass

# --- GPT Integration ---
# Once we have coordinates, we can call the GPT API if guide_text is not fetched yet.
if st.session_state.coords and st.session_state.guide_text is None:
    # Show loading
    st.session_state.fetching_guide = True
    st.info("Fetching guided tour from server...")
    lat, lon = st.session_state.coords

    # Call OpenAI API
    openai_api_key = st.secrets["openai"]["api_key"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    prompt = f"You are a historical tour guide. Provide a rich, detailed historical tour for the location at latitude {lat}, longitude {lon}. Explain what is historically significant about this place and the surrounding area."
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a highly knowledgeable historical tour guide."},
                     {"role": "user", "content": prompt}],
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

# --- Display Guide or Errors ---
if st.session_state.error:
    st.markdown(f'<div class="error-text">{st.session_state.error}</div>', unsafe_allow_html=True)
elif st.session_state.fetching_guide:
    st.info("Retrieving the guided tour content...")
elif st.session_state.guide_text:
    # Display the guided tour text
    st.markdown(f'<div class="guide-text">{st.session_state.guide_text}</div>', unsafe_allow_html=True)

    # --- TTS Control ---
    # We'll use the Web Speech API. We need JS code to handle play/pause.
    # We'll inject a hidden HTML block with JS that can read the text from a known element.
    # The buttons will trigger JS functions to control speech.
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

    # Buttons row
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    play_col, pause_col = st.columns([1,1], gap="medium")
    with play_col:
        if st.button("Play", key="play_button"):
            # JS call to start speech
            st.markdown("<script>playSpeech();</script>", unsafe_allow_html=True)
    with pause_col:
        if st.button("Pause", key="pause_button"):
            # JS call to pause speech
            st.markdown("<script>pauseSpeech();</script>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
