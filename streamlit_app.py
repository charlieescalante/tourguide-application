import streamlit as st
from streamlit_js_eval import streamlit_js_eval as st_js

# Streamlit app configuration
st.set_page_config(page_title="Geolocation App", layout="centered", page_icon="📍")

st.title("Geolocation App")

# Use JavaScript to get geolocation data
geolocation_data = st_js(
    "navigator.geolocation.getCurrentPosition((position) => position.coords)",
    timeout=5
)

if geolocation_data:
    latitude = geolocation_data.get("latitude", "N/A")
    longitude = geolocation_data.get("longitude", "N/A")
    
    st.success("Geolocation Retrieved Successfully!")
    st.write(f"**Latitude:** {latitude}")
    st.write(f"**Longitude:** {longitude}")
else:
    st.warning("Unable to retrieve geolocation. Please allow access to your location.")
