import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import requests

st.set_page_config(page_title="History Tour", layout="centered", page_icon="🗺️")

st.markdown('<h1 style="text-align: center;">History Tour</h1>', unsafe_allow_html=True)

coords = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => resolve(position.coords),
                (error) => reject({ error: error.message }),
                { timeout: 10000 }
            );
        } else {
            reject({ error: "Geolocation is not supported by this browser." });
        }
    });
    """
)

st.write("Raw geolocation data:", coords)

if coords:
    if "error" in coords:
        st.error(f"Geolocation error: {coords['error']}")
    else:
        latitude = coords.get("latitude")
        longitude = coords.get("longitude")
        if latitude and longitude:
            st.success(f"Your coordinates: {latitude}, {longitude}")
            # Add your OpenAI API integration here
        else:
            st.error("Failed to retrieve latitude and longitude.")
else:
    st.warning("No geolocation data received. Please try again.")
