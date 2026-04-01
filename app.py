import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Namma Nanban AI", page_icon="😎")
st.title("😎 Namma Nanban AI")

# --- Setup ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Standard Flash Model (Nichayamah work aagum)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Setup Error: {str(e)}")

slang = st.sidebar.selectbox("Slang Choose Pannunga:", ["Chennai", "Madurai", "Kongu"])
system_instructions = f"You are a funny friend from {slang}, Tamil Nadu. Speak in Tanglish. Use local slang like 'Mappillai', 'Thala', 'Gethu'. Be helpful and sarcastic."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enna thala, enna vishayam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Simple & Direct Call
            response = model.generate_content(f"{system_instructions} \nUser: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Response Error: {str(e)}")
