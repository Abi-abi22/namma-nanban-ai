import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Namma Nanban AI", page_icon="😎")
st.title("😎 Namma Nanban AI")
st.caption("Unga kooda jolly-ah pesa oru local nanban!")

# API Key from Secrets
try:
    API_KEY = st.secrets["AIzaSyADSe-HOa9AReIbNO1JsI_JkTmvN2PJbpk"]
    genai.configure(api_key=API_KEY)
    
    # Updated Model Name
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("API Key or Model setup-la problem thala! Secrets-ah check pannunga.")

# Slang selection
slang = st.sidebar.selectbox("Slang Choose Pannunga:", ["Chennai", "Madurai", "Kongu"])

# System prompt
system_instructions = f"You are a funny friend from {slang}, Tamil Nadu. Speak in Tanglish. Use local slang. Be sarcastic and helpful."

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enna thala, enna vishayam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    try:
        with st.chat_message("assistant"):
            # generate_content-la simple-ah prompt anuppalam
            response = model.generate_content(f"{system_instructions} \nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {str(e)}")
