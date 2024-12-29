import streamlit as st
from streamlit.components.v1 import html

# Streamlit app configuration
st.set_page_config(page_title="Geolocation App", layout="centered", page_icon="📍")

st.title("Geolocation App")

# JavaScript to get geolocation and display it directly in the app
geolocation_js = """
<script>
function getGeolocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                document.getElementById("latitude").innerText = latitude;
                document.getElementById("longitude").innerText = longitude;
            },
            (error) => {
                document.getElementById("output").innerText = "Unable to retrieve geolocation.";
            }
        );
    } else {
        document.getElementById("output").innerText = "Geolocation is not supported by this browser.";
    }
}
</script>
<button onclick="getGeolocation()">Get Geolocation</button>
<p>Latitude: <span id="latitude">N/A</span></p>
<p>Longitude: <span id="longitude">N/A</span></p>
<div id="output"></div>
"""

# Embed the HTML and JavaScript in the Streamlit app
html(geolocation_js, height=300)
