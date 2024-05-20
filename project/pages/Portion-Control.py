import os
import openai
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

# Set page configuration
st.set_page_config(page_title="Portion Control - Food Waste Watchers", layout="wide")

# Feature 2 content
st.markdown("# Portion Control 🍽️")
st.sidebar.markdown("## Portion Control")

# Set up your OpenAI API key from the environment variables
client = OpenAI(api_key="OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    # Open the PDF file
    pdf = fitz.open(stream=pdf_file.read())
    text = ""
    # Extract text from each page
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Prepare a brief description as an expert nutritionist specializing in adequeate portion sizes in order to reduce food waste. Then list the recommended portion sizes of the dish inputted. The response should be in a list format by ingredient suitable for individuals in the household. "},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Streamlit UI setup
st.title("Portion Control from PDF")
st.sidebar.title("Portion Control Assistant")

# File uploader allows user to add PDF
uploaded_pdf = st.file_uploader("Choose a PDF file containing an ingredient list", type=["pdf"])

if uploaded_pdf is not None:
    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(uploaded_pdf)
    # Display the extracted text
    st.text_area("Extracted text from the PDF:", extracted_text, height=300)

    # Generate portion size from extracted ingredients
    if st.button("Generate Portion Size"):
        # Create a prompt using the extracted text
        prompt = f"Here is a list of portion sizes from the uploaded PDF: {extracted_text}\nWhat is an adequate portion size using the dish inputted that is catered towards adults?"
        
        # Get a response from OpenAI
        portion = get_completion(prompt)
        st.markdown("## Generated Portion size:")
        st.write(portion)