import streamlit as st
from chain import explain_concept, generate_code
import time
from dataclasses import dataclass
import json
import markdown
import pdfkit
import os
import subprocess

USER = "user"
ASSISTANT = "ai"
CODE = "code ai"
MESSAGES = "messages"


@st.cache_data(show_spinner=False)
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


@st.cache_data()
def get_json():
    # Opening JSON file
    f = open("Data+Analysis+Concepts.json")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data


@st.cache_data()
def savePdf(res, code, concept):
    """
    Converts a Markdown string to a PDF file.

    Parameters:
    res (str), code (str): The Markdown text to convert.
    concept (str): The path to the output PDF file.
    """
    executable = (
        subprocess.run(["which", "wkhtmltopdf"], stdout=subprocess.PIPE)
        .stdout.decode()
        .strip()
    )
    config = pdfkit.configuration(wkhtmltopdf=bytes(executable, "utf-8"))

    # Convert Markdown to HTML
    html_text = markdown.markdown(res)
    html_text += "\n"
    html_text += markdown.markdown(code)

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html_text, configuration=config)
    return pdf


# Function to sending data to LLM model and recieve its response
def get_explaination(concept):
    explaination = explain_concept(concept)
    return explaination


# Function to sending data to LLM model and recieve its response
def get_code(concept):
    code, explaination = generate_code(concept)
    return code + "\n" + explaination


@dataclass
class Message:
    actor: str
    payload: str


# Streamlit app
def concept():
    st.title("Concept Explaination Session ⁉️")
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = [
            Message(
                actor=ASSISTANT,
                payload="Hi! Can i help you understand any concept?",
            )
        ]

    msg: Message
    for msg in st.session_state[MESSAGES]:
        st.chat_message(msg.actor).write(msg.payload)
    data = get_json()
    expander = st.sidebar.expander("Common Concepts")
    for index, item in enumerate(data):
        expander.write(item["data_analysis_concept"])

    concept: str = st.chat_input("Enter a concept")

    if concept:
        res = ""
        cod = ""
        st.session_state[MESSAGES].append(Message(actor=USER, payload=concept))
        st.chat_message(USER).write(concept)
        with st.spinner("Generating Explaination..."):
            response: str = get_explaination(concept)
        res += response
        st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
        st.chat_message(ASSISTANT).write(response)
        with st.spinner("Generating Code..."):
            response: str = get_code(concept)
        cod += response
        st.session_state[MESSAGES].append(Message(actor=CODE, payload=response))
        st.chat_message(name="coder", avatar="💻").markdown(response)
        # st.button(
        #     "Download Guide as PDF ⬇️", on_click=savePdf, args=[res, cod, concept]
        # )
        st.download_button(
            "Download Guide as PDF ⬇️",
            savePdf(res, cod, concept),
            file_name=concept.replace(" ", "") + ".pdf",
        )
