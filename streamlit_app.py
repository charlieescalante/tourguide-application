import streamlit as st
from streamlit_js_eval import streamlit_js_eval as st_js

# Streamlit app configuration
st.set_page_config(page_title="Geolocation App", layout="centered", page_icon="📍")

st.title("Geolocation App")

# Button to fetch geolocation
if st.button("Get Geolocation"):
    try:
        # Fetch geolocation data with a label
        location_data = st_js(
            "navigator.geolocation.getCurrentPosition((position) => position.coords)",
            key="get_geolocation",
            label="Fetching Geolocation"
        )

        if location_data:
            latitude = location_data.get("latitude", "N/A")
            longitude = location_data.get("longitude", "N/A")

            # Display results
            st.success("Geolocation Retrieved Successfully!")
            st.write(f"**Latitude:** {latitude}")
            st.write(f"**Longitude:** {longitude}")
        else:
            st.warning("Unable to retrieve geolocation. Please allow access to your location.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Click the button to fetch your geolocation.")
