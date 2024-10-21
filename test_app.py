import streamlit as st
from openai import OpenAI  # Test this specific import

st.write("Testing OpenAI import")

# Simple usage example (replace with your actual API key if needed)
try:
    client = OpenAI(api_key="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")
    st.write("OpenAI import successful!")
except Exception as e:
    st.write(f"Error: {e}")
