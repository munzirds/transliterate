import os
import streamlit as st
from openai import AzureOpenAI
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container


# Page configuration
st.set_page_config(
    page_title="Urdu to Hindi Transliterator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)
from arabic_support import support_arabic_text
support_arabic_text(components=[ "textarea"])


# Custom Dark Theme Styling
st.markdown("""
    <style>
        /* Main app background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #ffffff, #f2f4f8);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #e3e9f0 !important;
            color: black;
        }

        /* Headers */
        h1, h2, h3 {
            color: #228B22; /* Slightly darker green */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00FF7F, #228B22);
            color: black;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #228B22, #00FF7F);
            color: white;
        }

        /* Text areas */
        .stTextArea textarea {
            border-radius: 10px;
            background-color: #f8f9fa;
            color: black;
            font-size: 16px;
            min-height: 150px;
        }

        /* Urdu text style */
        .urdu-text {
            font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
            font-size: 24px;
            direction: rtl;
            text-align: center;
            line-height: 1.8;
            color: black;
        }

        /* Hindi text style */
        .hindi-text {
            font-family: 'Noto Sans Devanagari', 'Mangal', sans-serif;
            font-size: 24px;
            text-align: center;
            line-height: 1.8;
            color: black;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 15px;
            margin-top: 30px;
            color: #6c757d;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)


# Transliteration function
def transliterate_urdu(text):
    """Transliterates Urdu text into Hindi (Devanagari script) using Azure OpenAI API."""
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        
        deployment_name = os.getenv("AZURE_MODEL_DEPLOYMENT")

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a expert transliterator that accurately transliterates Urdu text to Hindi (Devanagari script)."},
                {"role": "user", "content": f"""
                Transliterate the following Urdu text into Hindi (Devanagari script) only.
                Provide output in the following structured format:
                
                Urdu: {text}
                Hindi: [Hindi transliteration here]

                Notes:
                - Use proper Hindi Devanagari script.
                - Do not translate, use the same words but in hindi script.
                """}
            ],
            max_tokens=150,
            temperature=0.3,
        )
        
        result = response.choices[0].message.content.strip()
        
        lines = [line.strip() for line in result.split('\n') if line.strip()]
        hindi_text = None
        
        for line in lines:
            if line.startswith("Hindi:"):
                hindi_text = line.replace("Hindi:", "").strip()
        
        return hindi_text

    except Exception as e:
        st.error(f"Error during transliteration: {e}")
        return None

# Sidebar
with st.sidebar:
    st.logo("nslogo.png", link="https://www.nucleosight.com")
    st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <h1 style="color:#00FF7F;">NS Urdu Transliterator</h1>
            <p style="color:#b3cde0;">Convert Urdu text to Hindi (Devanagari)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### How to Use")
    st.markdown("""
        1. Type or paste Urdu text
        2. Click 'Transliterate'
        3. See Hindi output
    """)
    
    st.markdown("### Example Phrases")
    example_phrases = [
        "کیا حال ہے؟",
        "آپ کا نام کیا ہے؟",
        "میں ٹھیک ہوں، شکریہ۔",
        "برائے مہربانی مدد کریں۔",
        "میں آپ سے محبت کرتا ہوں۔"
    ]
    
    for phrase in example_phrases:
        if st.button(phrase, key=f"example_{phrase}"):
            st.session_state.urdu_text = phrase

# Main Content
colored_header(
    label="Urdu to Hindi Transliterator",
    description="Powered by Nucleosight",
    color_name="green-70"
)

# Input container
with stylable_container(
    key="input_container",
    css_styles="""
        {
            background: #ffffff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
    """
):
    urdu_text = st.text_area(
        "اردو متن یہاں درج کریں",
        value=st.session_state.get("urdu_text", ""),
        height=150,
        key="urdu_input",
        help="Type or paste Urdu text here for Hindi transliteration"
    )
    
    col1, col2 = st.columns([1, 6])
    with col1:
        translate_btn = st.button("Transliterate", type="primary")
    with col2:
        if st.button("Clear"):
            st.session_state.urdu_text = ""
            st.session_state.hindi_result = ""
            st.rerun()

# Transliteration result
if translate_btn and urdu_text:
    with st.spinner("Transliterating..."):
        hindi_result = transliterate_urdu(urdu_text)
        
        if hindi_result:
            st.session_state.hindi_result = hindi_result
            st.session_state.urdu_text = urdu_text
        else:
            st.error("Transliteration failed. Please try again.")

if st.session_state.get("hindi_result"):
    st.markdown("### Results")

    # Urdu Text
    with stylable_container(
        key="urdu_card",
        css_styles="""
            {
                background: #ffffff;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
        """
    ):
        st.markdown("**Original Urdu Text**")
        st.markdown(f'<div class="urdu-text">{st.session_state.urdu_text}</div>', unsafe_allow_html=True)

    # Hindi Result
    with stylable_container(
        key="hindi_card",
        css_styles="""
            {
                background: #ffffff;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
        """
    ):
        st.markdown("**Hindi Transliteration**")
        st.markdown(f'<div class="hindi-text">{st.session_state.hindi_result}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Developed with ❤️ by <a href="https://www.nucleosight.com" style="color:#00FF7F;">Nucleosight</a></p>
    </div>
""", unsafe_allow_html=True)
