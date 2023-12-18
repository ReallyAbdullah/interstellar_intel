import streamlit as st
from question import get_df, get_QA_pairs
from vertex import init_sample, get_model, get_text_generation
from model_functions import create_qa_prompt
import re
import time


@st.cache_data(show_spinner=False)
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


@st.cache_data
def prepare_for_markdown(text):
    """
    Prepares a given text string for display using Markdown in Streamlit. This function
    ensures that the Markdown syntax is correctly applied and handles special characters,
    patterns, and indentation that might interfere with Markdown rendering.

    Parameters:
    text (str): The text to be formatted for Markdown.

    Returns:
    str: Formatted text suitable for Markdown rendering.
    """

    # Escape special Markdown characters like *, _, #, etc.
    text = re.sub(r"([*_#])", r"\\\1", text)

    # Ensure proper line breaks for Markdown (two spaces at the end of a line)
    text = re.sub(r"([^\n])\n", r"\1  \n", text)

    # Convert URLs to Markdown links (if not already formatted)
    url_pattern = r"(http[s]?://\S+)"
    text = re.sub(url_pattern, r"[\1](\1)", text)

    # Handle indentation for blockquotes, lists, etc.
    # Assuming blockquotes are represented with '>' at the start of a paragraph
    text = re.sub(r"\n\s*>", r"\n>", text)

    # Handle lists - replace any leading spaces before list items with a single space
    text = re.sub(r"\n\s*([-*])", r"\n\1", text)

    # Handling indented code blocks (assuming they start with 4 spaces)
    text = re.sub(r"\n {4}", r"\n    ", text)

    # Additional formatting rules can be added here as needed

    return text


@st.cache_data
def load_model():
    PROJECT_ID = "rex-assistant-407413"
    REGION = "europe-west4"
    init_sample(project_id=PROJECT_ID, location=LOCATION)


# Function to sending data to LLM model and recieve its response
def ask_llm_model(question, model_answer, id, user_response):
    prompt = create_qa_prompt(question, model_answer, id, user_response)
    return get_text_generation(prompt=prompt)


@st.cache_data
def load_qa_pairs():
    df = get_df()
    # List of question and model answer pairs
    return get_QA_pairs(1, df["ID"].unique(), df)


qa_pairs = load_qa_pairs()


# Streamlit app
def question_module():
    st.title("Interview Q/A Session ⁉️")
    for qa in qa_pairs:
        for index, pair in qa.iterrows():
            question_key = f"response_{index}"  # Unique key for each question

            # Initialize session state for each question
            if question_key not in st.session_state:
                st.session_state[question_key] = None

            st.subheader(pair["Question"] + "[ Category: " + pair["ID"] + "]")
            user_response = st.text_input("Your answer", key=pair["Question"])

            if user_response and st.session_state[question_key] is None:
                # Update session state with LLM response
                st.session_state[question_key] = ask_llm_model(
                    pair["Question"], pair["Answer"], pair["ID"], user_response
                )
            if st.session_state[question_key]:
                st.write("🤖 Interview Assistant:")
                lines = st.session_state[question_key].split("\n")
                for line in lines:
                    # st.markdown(line, unsafe_allow_html=True)
                    typewriter(line, 10)
