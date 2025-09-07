import streamlit as st
import urllib.parse

from pipeline import detect_pii
from utils import mask_text

st.set_page_config(page_title="PII Masker", layout="centered")

st.title("🔒 PII Masking Web Tool")

st.warning(
    "⚠️ This tool does **not** use any Large Language Models (LLMs). "
    "It only performs PII detection and masking to help you make prompts "
    "GDPR, SOC 2 and other data-privacy standard compliant before sending them to an LLM."
)

# ---- Input ----
input_text = st.text_area("Enter text to process:", height=150)

if st.button("Mask PII"):
    if input_text.strip() == "":
        st.warning("Please enter some text to process.")
    else:
        with st.spinner("Detecting sensitive information..."):
            entities = detect_pii(input_text)
            masked = mask_text(input_text, entities)

        # ---- Processed Output ----
        st.subheader("Processed Prompt")
        st.code(masked, language="text")

        # URL encode
        encoded_prompt = urllib.parse.quote(masked)

        # External links
        chatgpt_url = f"https://chat.openai.com/?q={encoded_prompt}"
        perplexity_url = f"https://www.perplexity.ai/search?q={encoded_prompt}"

        st.markdown("### Your Favorite AI Chatbots")
        col1, col2 = st.columns([1, 1], gap="small")
        btn_style = "margin:0 2px 0 0; background:#10a37f;color:white;padding:0.5rem 0.7rem;border:none;border-radius:6px;font-size:1rem;cursor:pointer;"
        btn_style2 = "margin:0 0 0 2px; background:#5f63ff;color:white;padding:0.5rem 0.7rem;border:none;border-radius:6px;font-size:1rem;cursor:pointer;"
        with col1:
            st.markdown(
                f'<a href="{chatgpt_url}" target="_blank"><button style="{btn_style}">Open in ChatGPT</button></a>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<a href="{perplexity_url}" target="_blank"><button style="{btn_style2}">Open in Perplexity AI</button></a>',
                unsafe_allow_html=True,
            )

        # ---- Entities ----
        st.subheader("🔍 Detected Entities")
        if entities:
            with st.expander("Show Detected Entities", expanded=False):
                st.markdown(
                    "<ul>"
                    + "\n".join(
                        [
                            f"<li><b>{ent['type']}</b>: <code>{ent['text']}</code> (score={ent['score']:.2f})</li>"
                            for ent in entities
                        ]
                    )
                    + "</ul>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No PII detected.")

# Close main container
st.markdown("</div>", unsafe_allow_html=True)
