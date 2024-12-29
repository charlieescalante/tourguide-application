import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.title("Geolocation App")

# Invoke the geolocation component
location = streamlit_geolocation()

# Check if location data is available
if location:
    st.success("Geolocation Retrieved Successfully!")
    st.write(f"**Latitude:** {location['latitude']}")
    st.write(f"**Longitude:** {location['longitude']}")
else:
    st.warning("Click the button to fetch your geolocation.")
