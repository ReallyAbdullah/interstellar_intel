import streamlit as st
from qa import question_module  # Import the app1 function
from caseStudy import cs  # Import the app2 function
from concept_chat import concept
from behavQA import bq

# Define the navigation structure
st.sidebar.title("Navigation")
app_choice = st.sidebar.selectbox(
    "Choose the app to view",
    ("Question Answer", "Case Study", "Concept Explaination", "Behavioural Questions"),
)

# Render the chosen app
if app_choice == "Question Answer":
    question_module()
elif app_choice == "Case Study":
    cs()
elif app_choice == "Concept Explaination":
    concept()
elif app_choice == "Behavioural Questions":
    bq()
