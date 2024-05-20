import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import openai
import os


# Function to encode image as base64
def encode_image(image, max_image=512):
    with Image.open(image) as img:
        width, height = img.size
        max_dim = max(width, height)
        if max_dim > max_image:
            scale_factor = max_image / max_dim
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

# Streamlit interface with updated color theme and emojis
st.set_page_config(page_title="🍳🥗 Recipe Creation from Image 🥘📸", layout="wide")
st.markdown("""
    <style>
        /* Main page styling */
        .reportview-container .main .block-container{
            padding-top: 5rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 5rem;
        }
        
        /* Color theme */
        :root {
            --primary: #8B0000; /* Deep red */
            --bg-color: #FFF8DC; /* Creamy off-white, cornsilk */
            --secondary-bg-color: #F5FFFA; /* Mint cream */
            --text-color: #4F4F4F; /* Dark gray */
            --accent-color: #90EE90; /* Light green */
            --font: 'sans serif';
        }
        
        header .decoration {
            background-color: var(--primary);
        }
        
        .stApp {
            background-color: var(--secondary-bg-color);
        }
        
        /* Streamlit components and text color */
        .reportview-container .main, .reportview-container .main .block-container {
            color: var(--text-color);
            background-color: var(--bg-color);
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: var(--accent-color);
            border-right: 2px solid var(--primary);
        }
        
        /* Button color */
        .stButton>button {
            color: var(--bg-color);
            background-color: var(--primary);
            border-radius: 20px;
            border: none;
        }

        /* Links color */
        a {
            color: var(--primary);
        }

    </style>
""", unsafe_allow_html=True)

# Page header with emoji
st.markdown("# Recipe Creation from Image 🥒🍅🍽️")
st.sidebar.markdown("## 🍳 Upload your image and get recipe suggestions 🥘")

# ... Rest of your code ...


# Streamlit form for image upload
uploaded_image = st.file_uploader("Upload an image of your fridge to get the most out of your ingredients.", type=["jpg", "jpeg", "png"])
if uploaded_image:
    with st.spinner('Processing image...'):
        # Encode the uploaded image as base64
        encoded_string = encode_image(uploaded_image)
        # Rest of your code remains the same...

        # System prompt to instruct GPT model about its role
        system_prompt = ("You are an expert assistant. When given an image of ingredients, "
                         "your job is to suggest recipes that can be made from those ingredients, "
                         "including calorie count for each recipe.")

        user_prompt = ("Given these ingredients, what are some recipes I can make? "
                       "Please include calorie counts.")

        # Make the API call to OpenAI
        apiresponse = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded_string}"},
                        },
                    ],
                },
            ],
            max_tokens=500,
        )

        # Display the result
        chat_completion = apiresponse.choices[0].message.content
        st.write("Recipe suggestions based on your image:")
        st.write(chat_completion)