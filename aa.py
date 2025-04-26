import os
import streamlit as st
from openai import AzureOpenAI

# Page configuration
st.set_page_config(
    page_title="Urdu to Hindi Transliterator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'urdu_text' not in st.session_state:
    st.session_state.urdu_text = ""
if 'hindi_result' not in st.session_state:
    st.session_state.hindi_result = ""

# Light theme styling
st.markdown("""
    <style>
        body { color: #2d3436; background-color: #ffffff; }
        .stTextArea textarea { 
            font-size: 18px; 
            min-height: 150px;
            color: #2d3436 !important;
            background-color: #f8f9fa !important;
        }
        .result-box { 
            padding: 20px; 
            border-radius: 10px; 
            background: #ffffff; 
            margin: 15px 0;
            border: 1px solid #dfe6e9;
        }
        .footer { 
            text-align: center; 
            margin-top: 30px; 
            color: #636e72; 
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2d3436 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            border-right: 1px solid #dfe6e9;
        }
        .stButton>button {
            background-color: #ffffff !important;
            color: #2d3436 !important;
            border: 1px solid #2d3436 !important;
        }
        .stButton>button:hover {
            background-color: #f8f9fa !important;
            color: #2d3436 !important;
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

# Main interface
st.title("Urdu to Hindi Transliterator")
st.markdown("---")

# Input area
urdu_text = st.text_area(
    "Enter Urdu text:",
    value=st.session_state.urdu_text,
    height=150
)

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Transliterate"):
        with st.spinner("Processing..."):
            st.session_state.hindi_result = transliterate_urdu(urdu_text) or ""
with col2:
    if st.button("Clear"):
        st.session_state.urdu_text = ""
        st.session_state.hindi_result = ""

# Display results
if st.session_state.hindi_result:
    st.markdown("### Results")
    
    st.markdown(f"""
        <div class='result-box'>
            <b>Original Urdu</b><br>
            <div style='font-size: 20px; margin-top: 10px;'>{st.session_state.urdu_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='result-box'>
            <b>Hindi Transliteration</b><br>
            <div style='font-size: 20px; margin-top: 10px;'>{st.session_state.hindi_result}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div class='footer'>Developed by "
            "<a href='https://nucleosight.com' style='color: #2d3436;'>Nucleosight</a></div>", 
            unsafe_allow_html=True)
