import streamlit as st
from question import get_df, get_QA_pairs
from vertex import init_sample, get_model, get_text_generation
from model_functions import create_qa_prompt


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
def main():
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
                st.write("🤖 Interview Assistant:", st.session_state[question_key])


if __name__ == "__main__":
    main()
