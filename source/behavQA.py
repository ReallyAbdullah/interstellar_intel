import streamlit as st
from question import read_behavioural_questions
from vertex import init_sample, get_model, get_text_generation
from model_functions import create_bq_prompt
import time
from chain import construct_star_chain, run_star_chain


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
    question,
    response,
    expected_elements,
    feedback,
    user_answer,
):
    prompt = create_bq_prompt(
        question,
        response,
        expected_elements,
        feedback,
        user_answer,
    )
    return get_text_generation(prompt=prompt)


@st.cache_resource(show_spinner=False)
def get_chain():
    return construct_star_chain()


@st.cache_data
def load_bq_objs():
    # List of case study objects
    return read_behavioural_questions()


bq_obj = load_bq_objs()
star_chain = get_chain()


# Streamlit app
def behavq():
    st.title("Interview Behavioural Question and STAR Analysis Session ⁉️")
    for index, bq in enumerate(bq_obj):
        bq_key = f"B response_{index}"  # Unique key for each case study
        # Initialize session state for each question
        if bq_key not in st.session_state:
            st.session_state[bq_key] = None

        st.subheader(bq["question"])
        st.caption("Ideas to include: " + ", ".join(bq["expected_elements"]))
        user_response = st.text_input("Your answer", key=bq["question"])

        if user_response and st.session_state[bq_key] is None:
            # Corrected call to ask_llm_model
            analysis = ask_llm_model(
                bq["question"],
                bq["response"],
                ", ".join(bq["expected_elements"]),
                bq["feedback"],
                user_response,
            )
            final_response = (
                analysis
                + "\n*STAR Analysis*\n"
                + run_star_chain(
                    user_response,
                    bq["question"],
                    ", ".join(bq["expected_elements"]),
                    star_chain,
                    analysis,
                )
            )
            st.session_state[bq_key] = final_response

        if st.session_state[bq_key]:
            st.write("🤖 Interview Assistant:")
            lines = st.session_state[bq_key].split("\n")
            for line in lines:
                # st.markdown(line, unsafe_allow_html=True)
                typewriter(line, 10)
