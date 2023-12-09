import requests
from typing import List


def create_qa_prompt(
    question: str,
    answer: str,
    topic: str,
    user_answer: str = "Couldn't Answer",
) -> str:
    """
    Creates a detailed prompt for language model feedback analysis based on a QA pair and user response.

    Parameters:
    question (str): The question to be analyzed.
    answer (str): The correct answer to the question.
    topic (str): The topic or category of the question.
    user_answer (str): The user's response to the question. Default is a placeholder text.

    Returns:
    str: A detailed prompt for feedback analysis.
    """

    prompt = f"""
    As an Expert Data Analyst Interview Preparation Assistant
    Evaluate the following user response to a question and provide personalized feedback for improvement.
    Incase the user couldn't answer, act motivational and say "Let me help you understand this " and then provide a step by step explaination of the solution for maximum undestanding.

    Question: {question}
    Topic: {topic}

    Correct Answer: {answer}

    User's Answer: {user_answer}

    Feedback Request: Please analyze the user's answer in comparison to the correct answer. Highlight any 
    inaccuracies, misunderstandings, or areas of improvement in the user's response. Provide constructive 
    feedback and suggestions on how the user can deepen their understanding of the topic and improve their 
    approach to answering similar questions.

    Strictly follow the following Feedback Structure:
    Is answer Correct/Incorrect/Partially correct
    How is the answer Correct/Incorrect/Partially correct
    What can be done to improve the response
    Incase of a question involving code/sql provide useful code snippet for better understanding
    Provide a model answer for maximum understanding
    """

    return prompt


# def create_cs_prompt(
#     use_case: str,
#     business_requirements: str,
#     technical_requirements: str,
#     question: str,
#     user_answer: str = "Couldn't Answer",
# ) -> str:
