import streamlit as st
from streamlit.components.v1 import html

# Streamlit app configuration
st.set_page_config(page_title="Geolocation App", layout="centered", page_icon="📍")

st.title("Geolocation App")

# JavaScript code to get geolocation
geolocation_js = """
<script>
function sendGeolocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const output = `Latitude: ${latitude}, Longitude: ${longitude}`;
                document.getElementById("output").innerText = output;
                Streamlit.setComponentValue({latitude: latitude, longitude: longitude});
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
<button onclick="sendGeolocation()">Get Geolocation</button>
<div id="output"></div>
"""

# Display the HTML and JavaScript
location_data = html(geolocation_js, height=200)

# Display results if available
if location_data:
    st.success("Geolocation Retrieved Successfully!")
    st.write(f"**Latitude:** {location_data['latitude']}")
    st.write(f"**Longitude:** {location_data['longitude']}")
else:
    st.warning("Click the button to fetch your geolocation.")
