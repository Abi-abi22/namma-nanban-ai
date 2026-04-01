import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Namma Nanban AI", page_icon="😎")
st.title("😎 Namma Nanban AI")
st.caption("Unga kooda jolly-ah pesa oru local nanban!")

# --- Setup with Multi-Model Check ---
if "model_name" not in st.session_state:
    st.session_state.model_name = None

def initialize_ai():
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        
        # Intha list-la irukira models-ah onnu onna check pannum
        models_to_try = [
            'gemini-1.5-flash', 
            'models/gemini-1.5-flash', 
            'gemini-1.5-flash-latest', 
            'gemini-pro'
        ]
        
        for m in models_to_try:
            try:
                test_model = genai.GenerativeModel(m)
                # Oru chinna test call - Work aagutha nu paaka
                test_model.generate_content("hi", generation_config={"max_output_tokens": 1})
                st.session_state.model_name = m
                return test_model
            except Exception:
                continue
        return None
    except Exception as e:
        st.error(f"Secret Key Error: {str(e)}")
        return None

model = initialize_ai()

if model is None:
    st.error("Thala, entha model-um work aagala! Unga API Key 'Leaked' aagi block aayirukkum. Please [Google AI Studio](https://aistudio.google.com/)-la oru PUDHU KEY create panni Secrets-la update pannunga.")
else:
    # --- Sidebar & Chat Logic ---
    slang = st.sidebar.selectbox("Slang Choose Pannunga:", ["Chennai", "Madurai", "Kongu"])
    st.sidebar.success(f"Using Model: {st.session_state.model_name}")
    
    system_instructions = f"You are a funny friend from {slang}, Tamil Nadu. Speak in Tanglish. Use local slang. Be helpful and sarcastic."

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
                full_prompt = f"{system_instructions} \nUser: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Response Error: {str(e)}")
