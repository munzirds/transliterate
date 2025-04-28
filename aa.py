import os
import time
import streamlit as st
from openai import AzureOpenAI
from functools import lru_cache
from langdetect import detect
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as indic_transliterate

# Page configuration
st.set_page_config(
    page_title="Urdu to Hindi Transliterator",
    page_icon="🌐",
    layout="wide",
)

# Check environment variables
def check_env_vars():
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_API_VERSION", "AZURE_ENDPOINT", "AZURE_MODEL_DEPLOYMENT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        st.error(f"Missing environment variables: {', '.join(missing_vars)}")
        st.stop()

check_env_vars()

# Initialize session state
if 'urdu_text' not in st.session_state:
    st.session_state.urdu_text = ""
if 'hindi_result' not in st.session_state:
    st.session_state.hindi_result = ""
if 'use_typing_effect' not in st.session_state:
    st.session_state.use_typing_effect = True

# Global styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Poppins:wght@300;400;600&display=swap');
        :root {
            --primary-bg: #f0f4f8;
            --text-color: #2d3436;
            --border-color: #dfe6e9;
            --accent-color: #0984e3;
            --button-bg: #2d3436;
        }
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: var(--primary-bg);
            color: var(--text-color);
        }
        .stTextArea textarea {
            font-size: 18px;
            min-height: 180px;
            background-color: #ffffff;
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s ease;
        }
        .stTextArea textarea:focus {
            border-color: var(--accent-color);
            box-shadow: 0 0 0 0.2rem rgba(9, 132, 227, 0.25);
        }
        .result-box {
            background: #ffffff;
            padding: 25px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid var(--border-color);
            animation: fadeIn 1s ease-in-out;
        }
        .urdu-text {
            font-family: 'Noto Nastaliq Urdu', serif;
            font-size: 28px;
            color: #34495e;
            margin-top: 10px;
            direction: rtl;
            text-align: right;
            white-space: pre-wrap;
        }
        .hindi-text {
            font-size: 26px;
            color: var(--text-color);
            margin-top: 10px;
            white-space: pre-wrap;
        }
        .stButton>button {
            background-color: var(--button-bg);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: var(--accent-color);
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 40px;
            color: #636e72;
        }
        @keyframes fadeIn {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)

@lru_cache(maxsize=100)
def transliterate_urdu(text):
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.geten v("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        response = client.chat.completions.create(
            model=os.getenv("AZURE_MODEL_DEPLOYMENT"),
            messages=[{
                "role": "user",
                "content": f"Transliterate this Urdu text to Hindi Devanagari script and return the result as a JSON object with a single key 'hindi' containing the transliterated text: {text}"
            }],
            temperature=0.3,
        )
        # Parse JSON response
        json_response = json.loads(response.choices[0].message.content.strip())
        if 'hindi' not in json_response:
            raise ValueError("JSON response does not contain 'hindi' key")
        return json_response['hindi']
    except Exception as e:
        st.error(f"Failed to transliterate. Please try again or contact support. Error: {str(e)[:100]}")
        with open("error_log.txt", "a") as f:
            f.write(f"{time.ctime()}: {str(e)}\n")
        return None

def rule_based_transliteration(text):
    try:
        return indic_transliterate(text, sanscript.URDU, sanscript.DEVANAGARI)
    except Exception:
        return transliterate_urdu(text)

def type_writer_effect(text, speed=0.05):
    typed_text = ""
    placeholder = st.empty()
    for char in text:
        typed_text += char
        placeholder.markdown(f"<div class='urdu-text'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)
    return typed_text

def type_writer_effect_hindi(text, speed=0.04):
    typed_text = ""
    placeholder = st.empty()
    for char in text:
        typed_text += char
        placeholder.markdown(f"<div class='hindi-text'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)
    return typed_text

def validate_input(text):
    if not text.strip():
        st.error("Please enter Urdu text.")
        return False
    if len(text) > 1000:
        st.error("Input text is too long. Please limit to 1000 characters.")
        return False
    try:
        if detect(text) != 'ur':
            st.warning("Input may not be Urdu. Proceed anyway?")
    except:
        pass
    return True

# Sidebar
with st.sidebar:
    st.image("nslogo.png", width=200)
    st.header("NS Urdu Transliterator")
    st.markdown("---")
    st.session_state.use_typing_effect = st.checkbox("Enable Typing Animation", value=True)
    example = st.selectbox("Try an example:", [
        "کیا حال ہے؟",
        "آپ کا نام کیا ہے؟",
        "میں ٹھیک ہوں، شکریہ۔",
        "برائے مہربانی مدد کریں۔",
        "میں آپ سے محبت کرتا ہوں۔"
    ])
    if st.button("Use Example"):
        st.session_state.urdu_text = example

# Main
st.title("🌐 Urdu to Hindi Transliterator")
st.markdown("Convert Urdu Nastaliq script into Hindi Devanagari effortlessly.")

st.markdown("---")

# Input
urdu_text = st.text_area(
    "Enter Urdu Text Below:",
    value=st.session_state.urdu_text,
    key="urdu_input",
    placeholder="Type or paste Urdu text here",
    help="Enter Urdu text in Nastaliq script to transliterate into Hindi Devanagari.",
)

# Action Buttons
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Transliterate"):
        if validate_input(urdu_text):
            with st.spinner("Transliterating..."):
                st.session_state.hindi_result = transliterate_urdu(urdu_text) or ""
with col2:
    if st.button("Clear"):
        st.session_state.urdu_text = ""
        st.session_state.hindi_result = ""

# Output Results
if st.session_state.hindi_result:
    st.markdown("### Result")
    
    st.markdown("<div class='result-box'><b>Original Urdu:</b>", unsafe_allow_html=True)
    if st.session_state.use_typing_effect:
        type_writer_effect(st.session_state.urdu_text, speed=0.07)
    else:
        st.markdown(f"<div class='urdu-text'>{st.session_state.urdu_text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='result-box'><b>Hindi Transliteration:</b>", unsafe_allow_html=True)
    if st.session_state.use_typing_effect:
        type_writer_effect_hindi(st.session_state.hindi_result, speed=0.06)
    else:
        st.markdown(f"<div class='hindi-text'>{st.session_state.hindi_result}</div>", unsafe_allow_html=True)
    
    st.button("Copy Hindi Text", on_click=lambda: st.write(f'<script>navigator.clipboard.writeText("{st.session_state.hindi_result}");</script>', unsafe_allow_html=True))
    st.download_button(
        label="Download Hindi Text",
        data=st.session_state.hindi_result,
        file_name="transliterated_hindi.txt",
        mime="text/plain"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div class='footer'>Developed with love by "
    "<a href='https://nucleosight.com' target='_blank'>Nucleosight</a></div>", 
    unsafe_allow_html=True
)
