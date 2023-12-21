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
    As an Expert Data Analyst Interview Preparation Assistant, your task is to evaluate and provide tailored feedback on a user's response to a data analysis question. Ensure your feedback is constructive, insightful, and aids in deepening the user's understanding of the subject. In cases where the user struggles to answer, adopt a motivational approach, guiding them through the solution with clear explanations.

    **Interview Question Context**:
    - Question: {question}
    - Topic: {topic}
    - Correct Answer: {answer}
    - User's Answer: {user_answer}

    **Your Analysis and Feedback Task**:
    1. **Assessment of User's Answer**:
    - Determine if the user's answer is Correct, Incorrect, or Partially Correct.
    - Elaborate on how the user's response aligns with these categories, citing specific examples or points from their answer.

    2. **Detailed Comparative Analysis**:
    - Compare the user's answer with the correct answer.
    - Identify specific areas where the user's understanding appears limited or inaccurate.
    - Highlight key differences in approach, methodology, or content between the user's response and the correct answer.

    3. **Constructive Feedback for Improvement**:
    - Offer clear, actionable advice on how the user can improve their understanding of the topic.
    - Suggest study materials, resources, or practice methods relevant to the topic.
    - If the question involves technical skills (like coding or SQL), include a relevant code snippet or example that aligns with best practices in data analysis.

    4. **Motivational Guidance**:
    - If the user's response indicates a lack of understanding, start with a motivational statement: "Let me help you understand this..."
    - Provide a step-by-step explanation of the solution, ensuring it's easy to follow and comprehend.

    5. **Model Answer**:
    - Conclude with a model answer that fully addresses the interview question, incorporating all necessary elements for a comprehensive and accurate response.

    **Response Format**: Use Markdown for clear and organized presentation of your feedback.
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
    **Case Study Context**:
    - Domain: {domain}
    - Question: {question}
    - Business Requirements: {business_requirements}
    - Technical Requirements: {technical_requirements}

    **User's Response**:
    - {user_answer}

    **Task for Data Analyst Interview Assistant**:
    - Analyze the user's response in the context of the provided case study.
    - Determine the accuracy and completeness of the user's answer based on the domain, business, and technical requirements.
    - Offer a detailed analysis that:
    - Identifies whether the answer is Correct/Incorrect/Partially Correct.
    - Elaborates on how and why the answer fits into one of these categories.
    - Provides specific insights into any gaps or inaccuracies in the user's understanding or approach.
    - Suggests clear and actionable steps for improvement, including tips, methodologies, or concepts the user should focus on.
    - In case of technical questions (involving code or SQL), include relevant code snippets or examples that demonstrate best practices or correct methodologies.
    - Conclude with a model answer that exemplifies an ideal response to the case study question, incorporating all necessary elements of a comprehensive and correct answer.

    **Data Analyst Interview Assistant Response Format**:
    - Begin with an overall assessment (Correct/Incorrect/Partially Correct).
    - Follow with a point-by-point comparison between the user's response and what an ideal response should entail.
    - Include practical advice for improvement and learning.
    - Provide additional resources or references if applicable.
    - Conclude with a model answer for the user to study and learn from.
    """

    return prompt


def create_bq_prompt(
    question: str,
    response: str,
    expected_elements: str,
    feedback: str,
    user_answer: str = "Couldn't Answer",
) -> str:
    """
    Creates a detailed prompt for language model feedback analysis based on a Behavioural Question Data Object and user response.

    Parameters:
    question (str): The question to be analyzed.
    response (str): The model correct answer to the question.
    expected_elements (str): The expected ideas to be discussed in the response.
    feedback (str): The expected basic feedback for the model answer.
    user_answer (str): The user's response to the question. Default is a placeholder text.

    Returns:
    str: A detailed prompt for feedback analysis.
    """

    prompt = f"""
    Act an Expert Data Analyst Interview Preparation Assistant

    The following is a Behavioural Question provided to a potential Data Analyst Candidate:

    Question: {question}
    Expected Elements: {expected_elements} -> These are the ideas/topics that need to be present directly or indirectly to answer correctly.

    Simplified Example of a Correct Answer: {response}
    Simplified Example Feedback for correct answer: {feedback}

    User's Answer: {user_answer}

    Evaluate the user's response to the behavioural question given the context of the Behavioural Question's expected elements.
    Incase the user couldn't answer, act motivational and start you response with "Let me help you understand this " and then provide a step by step explaination of the solution for the user to understant you thought process.

    Please analyze the user's answer in comparison to the correct answer. Highlight any 
    inaccuracies, misunderstandings, or areas of improvement in the user's response. Provide constructive 
    feedback and suggestions on how the user can deepen their understanding of the topic and improve their 
    approach to answering similar questions. You have to make sure that the user understands what a Data Analyst Interviewer is actually looking for in each question's response.

    Strictly follow the following Feedback Structure:
    Is the answer Poor/Mediocre/Good
    How is the answer Poor/Mediocre/Good
    3 Detailed Hypothetical examples of a Good Answer
    """

    return prompt
