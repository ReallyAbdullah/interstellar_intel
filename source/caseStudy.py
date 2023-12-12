import streamlit as st
from question import sample_data_elements, sample_data_by_requirements
from vertex import init_sample, get_model, get_text_generation
from model_functions import create_qa_prompt, create_cs_prompt
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
def load_model():
    PROJECT_ID = "rex-assistant-407413"
    REGION = "europe-west4"
    init_sample(project_id=PROJECT_ID, location=LOCATION)


# Function to sending data to LLM model and recieve its response
def ask_llm_model(
    domain,
    business_requirements,
    technical_requirements,
    question,
    model_answer,
    basic_feedback,
    user_answer,
):
    prompt = create_cs_prompt(
        domain,
        business_requirements,
        technical_requirements,
        question,
        model_answer,
        basic_feedback,
        user_answer,
    )
    return get_text_generation(prompt=prompt)


@st.cache_data
def load_cs_objs():
    # List of case study objects
    return sample_data_by_requirements(
        technical_reqs=["SQL", "Data Cleaning"], sample_size=3
    )


cs_obj = load_cs_objs()


# Streamlit app
def cs():
    st.title("Interview Case Study Session ⁉️")
    for index, cs in enumerate(cs_obj):
        cs_key = f"response_{index}"  # Unique key for each case study
        # Initialize session state for each question
        if cs_key not in st.session_state:
            st.session_state[cs_key] = None

        st.subheader(cs["question"] + " [ Topic: " + cs["domain"] + "]")
        st.caption("Business Req: " + ", ".join(cs["business_requirements"]))
        st.caption("Technical Req: " + ", ".join(cs["technical_requirements"]))
        user_response = st.text_input("Your answer", key=cs["question"])

        if user_response and st.session_state[cs_key] is None:
            # Corrected call to ask_llm_model
            st.session_state[cs_key] = ask_llm_model(
                cs["domain"],
                ", ".join(cs["business_requirements"]),
                ", ".join(cs["technical_requirements"]),
                cs["question"],
                cs["model_answer"],
                cs["basic_feedback"],
                user_response,
            )

        if st.session_state[cs_key]:
            st.write("🤖 Interview Assistant:")
            lines = st.session_state[cs_key].split("\n")
            for line in lines:
                # st.markdown(line, unsafe_allow_html=True)
                typewriter(line, 10)
