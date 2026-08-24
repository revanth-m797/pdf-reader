import streamlit as st
from google import genai
from pypdf import PdfReader
from PIL import Image
import numpy as np
import easyocr
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Document Summary Assistant",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📄 Document Summary Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload any digital PDF or scanned image to instantly extract data and generate smart summaries.</div>', unsafe_allow_html=True)

key = os.getenv("api_key")

if not key:
    st.error("⚠️ API Key Missing: Please add 'GEMINI_API_KEY' to your local .env file or your Streamlit secrets dashboard.")
    st.stop()
else:
    ai = genai.Client(api_key=key)

@st.cache_resource
def get_ocr():
    return easyocr.Reader(['en'], gpu=False)

ocr = get_ocr()

st.sidebar.header("🎯 Summary Settings")
size = st.sidebar.select_slider(
    "Choose Summary Depth:",
    options=["Short", "Medium", "Long"],
    value="Medium",
    help="Short: ~2-3 sentences. Medium: Comprehensive bullet points. Long: Exhaustive section-by-section breakdown."
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tech Stack:** Python, Streamlit, EasyOCR, Modern Google Gen AI SDK.")

file = st.file_uploader(
    "Drag and drop your file here or click browse", 
    type=["pdf", "png", "jpg", "jpeg"]
)

if file is not None:
    kind = file.type
    txt = ""
    
    tab1, tab2 = st.tabs(["✨ Generated Summary", "🔍 Extracted Raw Text"])

    with st.spinner("Extracting content from file... Please wait."):
        try:
            if "pdf" in kind:
                pdf = PdfReader(file)
                for pg in pdf.pages:
                    body = pg.extract_text()
                    if body:
                        txt += body + "\n"
                
                if not txt.strip():
                    st.warning("No embedded text found. This looks like a scanned PDF. Please extract pages as images or upload an image file.")
                    st.stop()
            
            else:
                img = Image.open(file)
                arr = np.array(img)
                
                lines = ocr.readtext(arr, detail=0)
                txt = "\n".join(lines)
                
                if not txt.strip():
                    st.warning("OCR complete, but no readable English text could be recognized in this image.")
                    st.stop()

        except Exception as err:
            st.error(f"Failed to extract document contents: {str(err)}")
            st.stop()

    with tab2:
        st.subheader("Raw Extracted Content")
        st.text_area("Plain Text Copy", value=txt, height=300, disabled=True)

    with tab1:
        if st.button("Generate Smart Summary", type="primary", use_container_width=True):
            with st.spinner("AI Engine is synthesizing content..."):
                try:
                    prompt = (
                        f"You are an expert document analysis assistant. Read the provided raw text data "
                        f"and construct a highly accurate, structured, and {size.lower()}-length summary.\n\n"
                        f"Requirements:\n"
                        f"1. Highlight all primary themes, main ideas, and core insights.\n"
                        f"2. Use clean Markdown bullet points and bold headers for maximum visual scannability.\n"
                        f"3. Do not assume facts; rely strictly on the provided context.\n\n"
                        f"Raw Extracted Document Text:\n{txt}"
                    )
                    
                    res = ai.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                    )
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📝 Smart Document Summary")
                    st.markdown(res.text)
                    
                except Exception as ex:
                    st.error(f"Error communicating with Generative AI Model: {str(ex)}")
