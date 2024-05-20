import streamlit as st
import fitz  
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

def get_completion(food_item, model="gpt-3.5-turbo"):
    prompt = (
        f"Provide detailed information about proper storage and average storage life for {food_item}. "
        "Include ways to maximize freshness. Identify any food items that are considered 'high-risk' for bacteria growth by labeling the food item with '⚠️ High-Risk Food Alert!'. Break each section up to clearly and easily read the infomration."
        "Provide an emoji next to the food item listed. If no emoji exists, do not include one."
    )
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": food_item},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Failed to get completion from OpenAI: {e}")
        return ""

image_url = "https://png.pngtree.com/png-vector/20221201/ourlarge/pngtree-food-storage-container-chalk-icon-linear-environmentally-waste-vector-png-image_42939600.jpg"

col1, col2 = st.columns([3, 1])
with col1:
    st.title("Smart Food Storage")
with col2:
    st.image(image_url, width=100)  

def display_information(food_item):
    ai_response = get_completion(food_item)
    st.write("Here is the information you requested :) ")
    st.write(ai_response)
    
# Streamlit UI components
food_item = st.text_input("Hello, please enter any food items you have :", '')
if st.button("GO !"):
    if food_item:
        display_information(food_item)
    else:
        st.error("Please enter a food item to proceed.")

with st.sidebar:
    st.markdown("<h1 style='color: red; font-size: 20px;'>IMPORTANT INFORMATION!!</h1>", unsafe_allow_html=True)
    st.write("For additional information on food safety and storage tips ")
    website_url = "https://www.betterhealth.vic.gov.au/health/healthyliving/food-safety-and-storage"
    st.markdown(f"please visit [this website]({website_url}) that provides useful information and advice.")

st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white; /* White text */
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green */
    }
</style>
""", unsafe_allow_html=True)