import streamlit as st
from qa import qam  # Import the app1 function
from caseStudy import cs  # Import the app2 function

# Define the navigation structure
st.sidebar.title("Navigation")
app_choice = st.sidebar.selectbox(
    "Choose the app to view", ("Question Answer", "Case Study")
)

# Render the chosen app
if app_choice == "Question Answer":
    qam()
elif app_choice == "Case Study":
    cs()
