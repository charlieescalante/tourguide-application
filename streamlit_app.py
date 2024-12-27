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

    # Process the response
    if response.status_code == 200:
        json_resp = response.json()
        guide_text = json_resp["choices"][0]["message"]["content"]
        st.session_state.guide_text
