import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION ---
PAGE_TITLE = "RepurposeAI"
PAGE_ICON = "🚀"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    .locked-box { padding: 1rem; border-radius: 0.5rem; background-color: #F8D7DA; color: #721C24; border: 1px solid #F5C6CB; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.header("💎 Upgrade to Pro")
license_key_input = st.sidebar.text_input("Enter License Key", type="password")
VALID_LICENSE_KEY = "PRO-2025-LAUNCH" 
is_premium = license_key_input == VALID_LICENSE_KEY

if is_premium:
    st.sidebar.success("✅ PRO Status: Active")
else:
    st.sidebar.warning("🔒 Status: Free Plan")
    st.sidebar.markdown("[Get a License Key ($9/mo)](#)")

# --- MAIN APP ---
st.title("🚀 RepurposeAI")
st.write("Turn one simple idea into viral content.")
topic = st.text_area("What is your topic?", height=100, placeholder="e.g., How to start a business...")
tone = st.select_slider("Select Tone", options=["Funny", "Casual", "Professional"], value="Casual")

def generate_content(prompt_type, topic, tone):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar!")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        if prompt_type == "twitter":
            prompt = f"Write a viral Twitter thread about '{topic}'. Tone: {tone}."
        elif prompt_type == "linkedin":
            prompt = f"Write a LinkedIn post about '{topic}'. Tone: {tone}."
        elif prompt_type == "newsletter":
            prompt = f"Write a newsletter about '{topic}'. Tone: {tone}."
        
        with st.spinner('AI is thinking...'):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

tab1, tab2, tab3 = st.tabs(["🐦 Twitter (Free)", "💼 LinkedIn (Pro)", "📧 Newsletter (Pro)"])

with tab1:
    if st.button("Generate Thread", key="btn_twitter"):
        if topic:
            result = generate_content("twitter", topic, tone)
            if result: st.write(result)

with tab2:
    if is_premium:
        if st.button("Generate LinkedIn", key="btn_linkedin"):
            if topic:
                result = generate_content("linkedin", topic, tone)
                if result: st.write(result)
    else:
        st.markdown("<div class='locked-box'>🔒 Upgrade to unlock LinkedIn</div>", unsafe_allow_html=True)

with tab3:
    if is_premium:
        if st.button("Generate Newsletter", key="btn_newsletter"):
            if topic:
                result = generate_content("newsletter", topic, tone)
                if result: st.write(result)
    else:
        st.markdown("<div class='locked-box'>🔒 Upgrade to unlock Newsletters</div>", unsafe_allow_html=True)
