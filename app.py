import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Namma Nanban AI", page_icon="😎")
st.title("😎 Namma Nanban AI")
st.caption("Unga kooda jolly-ah pesa oru local nanban!")

# API Key - Itha appram safe-ah vachukalam, ippo testing-ku direct-ah kodu
API_KEY = "AIzaSyADSe-HOa9AReIbNO1JsI_JkTmvN2PJbpk" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Persona/Slang selection
slang = st.sidebar.selectbox("Slang Choose Pannunga:", ["Chennai", "Madurai", "Kongu"])

# System prompt based on slang
system_instructions = f"You are a funny friend from {slang}, Tamil Nadu. Speak in Tanglish. Use local slang. Be sarcastic and helpful."

# Chat history initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enna thala, enna vishayam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        full_prompt = f"{system_instructions} \nUser: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
