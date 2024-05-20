import streamlit as st

# Set the title and initial configuration for the main page
st.set_page_config(page_title="🍳🥗 Food Waste Watchers 🥘📸", layout="wide")

# Main page title and sidebar title
st.markdown("# Food Waste Watchers Main Page 🎈")
st.sidebar.markdown("# Main Page Navigation 🧭")

# Introduction message for the main page
intro_message = ("Welcome to Food Waste Watchers! This is your starting point to explore "
                 "different tools to manage food waste efficiently. 🎉 Use the sidebar to navigate through the "
                 "features and find tools for recipe creation, portion control, and food "
                 "storage assistance.")
st.write(intro_message)

# Add navigation links to the sidebar for each feature
st.sidebar.markdown("## Features")
st.sidebar.markdown("- 🥘 [Recipe Creation]")
st.sidebar.markdown("- 🍽️ [Portion Control]")
st.sidebar.markdown("- 🗃️ [Food Storage Assist Bot]")

# Placeholder where you can add any additional content or instructions
st.write("Select a feature from the sidebar to get started!")

# Note: The actual navigation will happen through the sidebar automatically.
