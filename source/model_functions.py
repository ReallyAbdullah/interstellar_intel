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
    Is answer Correct/Incorrect/Partially Correct
    How is the answer Correct/Incorrect/Partially correct
    What can be done to improve the response
    Incase of a question involving code/sql provide useful code snippet for better understanding
    Provide a model answer for maximum understanding

    Final Considerations: Generate the response with Markdown.
    """

    return prompt


def create_cs_prompt(
    domain: str,
    business_requirements: str,
    technical_requirements: str,
    question: str,
    model_answer: str,
    basic_feedback: str,
    user_answer: str = "Couldn't Answer",
) -> str:
    """
    Creates a detailed prompt for language model feedback analysis based on a Case Study Data Object and user response.

    Parameters:
    domain (str): The topic or category of the case study.
    business_requirements (str): The Business requirements related to the case study.
    technical_requirements (str): The technical requirements related to the case study.
    question (str): The question to be analyzed.
    model answer (str): The correct answer to the question.
    basic_feedback (str): The expected basic feedback for the model answer.
    user_answer (str): The user's response to the question. Default is a placeholder text.

    Returns:
    str: A detailed prompt for feedback analysis.
    """

    prompt = f"""
    Act an Expert Data Analyst Interview Preparation Assistant

    The following is a case study provided to a potential Data Analyst Candidate:

    Domiain: {domain}
    Question: {question}
    Business Requirements: {business_requirements}
    Technical Requirements: {technical_requirements}

    Simplified Example of a Correct Answer: {model_answer}
    Simplified Example Feedback for correct answer: {basic_feedback}

    User's Answer: {user_answer}

    Evaluate the user's response to the case study question given the context of the Case study domain, business requirements and technical requirements.
    Incase the user couldn't answer, act motivational and start you response with "Let me help you understand this " and then provide a step by step explaination of the solution for the user to understant you thought process.

    Please analyze the user's answer in comparison to the correct answer. Highlight any 
    inaccuracies, misunderstandings, or areas of improvement in the user's response. Provide constructive 
    feedback and suggestions on how the user can deepen their understanding of the topic and improve their 
    approach to answering similar questions.

    Strictly follow the following Feedback Structure:
    Is the answer Correct/Incorrect/Partially correct
    How is the answer Correct/Incorrect/Partially correct
    What can be done to improve the response
    Incase of a question involving code/sql provide useful code snippet for better understanding
    Provide a model answer for maximum understanding
    """

    return prompt
