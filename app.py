import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Namma Nanban AI", page_icon="😎")
st.title("😎 Namma Nanban AI")

# --- Model Setup ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Safest model name that works everywhere
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Setup Error: {str(e)}")

# --- Sidebar Slang Selection ---
slang = st.sidebar.selectbox("Slang Choose Pannunga:", ["Chennai", "Madurai", "Kongu"])
system_instructions = f"You are a funny friend from {slang}, Tamil Nadu. Speak in Tanglish. Use local slang. Be helpful and sarcastic."

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input & AI Response ---
if prompt := st.chat_input("Enna thala, enna vishayam?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Model response
            full_prompt = f"{system_instructions} \nUser: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {str(e)}")
        # Debug: list available models to help you find the right name
        st.write("Available models list:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                st.write(f"- {m.name}")
