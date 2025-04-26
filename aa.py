import os
import time
import streamlit as st
from openai import AzureOpenAI

# Page configuration
st.set_page_config(
    page_title="Urdu to Hindi Transliterator",
    page_icon="🌐",
    layout="wide",
    
)

# Initialize session state
if 'urdu_text' not in st.session_state:
    st.session_state.urdu_text = ""
if 'hindi_result' not in st.session_state:
    st.session_state.hindi_result = ""
if 'show_typing' not in st.session_state:
    st.session_state.show_typing = False

# Global styles: shimmer + Noto Nastaliq + animations
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f0f4f8;
            color: #2d3436;
        }
        .stTextArea textarea {
            font-size: 18px;
            min-height: 180px;
            background-color: #ffffff;
            color: #2d3436;
            border: 1px solid #dcdde1;
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s ease;
        }
        .stTextArea textarea:focus {
            border-color: #0984e3;
            box-shadow: 0 0 0 0.2rem rgba(9, 132, 227, 0.25);
        }
        .result-box {
            background: #ffffff;
            padding: 25px;
            margin-top: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #dfe6e9;
            animation: fadeIn 1s ease-in-out;
            position: relative;
            overflow: hidden;
        }
        .result-box::after {
            content: "";
            position: absolute;
            top: 0;
            left: -150px;
            height: 100%;
            width: 150px;
            background: linear-gradient(120deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.5) 50%, rgba(255,255,255,0.1) 100%);
            animation: shimmer 2s infinite;
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
            color: #2d3436;
            margin-top: 10px;
            white-space: pre-wrap;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2d3436;
            font-weight: 600;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #dfe6e9;
        }
        .stButton>button {
            background-color: #2d3436;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0984e3;
            color: white;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 40px;
            color: #636e72;
        }
        a {
            color: #0984e3;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }

        @keyframes fadeIn {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }

        @keyframes shimmer {
            0% { left: -150px; }
            100% { left: 100%; }
        }
    </style>
""", unsafe_allow_html=True)

def transliterate_urdu(text):
    """Simplified transliteration function"""
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_MODEL_DEPLOYMENT"),
            messages=[{
                "role": "user",
                "content": f"Transliterate this Urdu text to Hindi Devanagari script: {text}"
            }],
            temperature=0.3,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def type_writer_effect(text, speed=0.05):
    """Simulate typing animation."""
    typed_text = ""
    placeholder = st.empty()
    for char in text:
        typed_text += char
        placeholder.markdown(f"<div class='urdu-text'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)
    return typed_text

def type_writer_effect_hindi(text, speed=0.04):
    """Hindi typing animation."""
    typed_text = ""
    placeholder = st.empty()
    for char in text:
        typed_text += char
        placeholder.markdown(f"<div class='hindi-text'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(speed)
    return typed_text

# Sidebar
with st.sidebar:
    st.image("nslogo.png", width=200)
    st.header("NS Urdu Transliterator")
    st.markdown("---")
    
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
)

# Action Buttons
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Transliterate"):
        with st.spinner("Transliterating..."):
            st.session_state.hindi_result = transliterate_urdu(urdu_text) or ""
            st.session_state.show_typing = True
with col2:
    if st.button("Clear"):
        st.session_state.urdu_text = ""
        st.session_state.hindi_result = ""
        st.session_state.show_typing = False

# Output Results
if st.session_state.hindi_result:
    st.markdown("### Result")
    
    st.markdown("<div class='result-box'><b>Original Urdu:</b>", unsafe_allow_html=True)
    if st.session_state.show_typing:
        type_writer_effect(st.session_state.urdu_text, speed=0.07)
    else:
        st.markdown(f"<div class='urdu-text'>{st.session_state.urdu_text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='result-box'><b>Hindi Transliteration:</b>", unsafe_allow_html=True)
    if st.session_state.show_typing:
        type_writer_effect_hindi(st.session_state.hindi_result, speed=0.06)
    else:
        st.markdown(f"<div class='hindi-text'>{st.session_state.hindi_result}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div class='footer'>Developed with love by "
    "<a href='https://nucleosight.com' target='_blank'>Nucleosight</a></div>", 
    unsafe_allow_html=True
        )
