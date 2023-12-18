import pandas as pd
from typing import List, Dict, Any
import string
import json
import random


def get_df() -> pd.DataFrame:
    """
    Reads a CSV file containing a question database and processes the 'ID' column.

    The function reads data from a file named 'QuestionDatabase.csv'. It assumes that the 'ID'
    column in this file contains alphanumeric values. The function strips trailing digits from the
    'ID' column values to standardize them.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data from 'QuestionDatabase.csv'.

    Raises:
    FileNotFoundError: If 'QuestionDatabase.csv' does not exist in the working directory.
    """
    print("Reading Database of Questions...")
    # Attempt to read the CSV file
    try:
        df = pd.read_csv("QuestionDatabase.csv")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "The file 'QuestionDatabase.csv' was not found in the working directory."
        ) from e

    # Process the 'ID' column by stripping trailing digits
    df["ID"] = df["ID"].str.rstrip(string.digits)

    return df


def get_QA_pairs(
    question_count: int, question_categories: List[str], df: pd.DataFrame
) -> List[pd.DataFrame]:
    """
    Generate a list of dataframes containing question-answer pairs based on specified categories.

    Parameters:
    question_count (int): The number of question-answer pairs to retrieve per category.
    question_categories (List[str]): A list of categories to filter the question-answer pairs.
    df (pd.DataFrame): The dataframe from which to retrieve the question-answer pairs.
                       It's expected to contain an 'ID' column for filtering by category.

    Returns:
    List[pd.DataFrame]: A list of dataframes, each containing a sample of question-answer pairs for a given category.

    Raises:
    ValueError: If 'question_count' is not positive.
    """

    if question_count <= 0:
        raise ValueError("question_count must be a positive integer")

    qa_pairs = []
    for category in question_categories:
        # Filtering the dataframe by category and sampling
        sampled_pairs = df[df["ID"] == category].sample(n=question_count)
        qa_pairs.append(sampled_pairs)

    return qa_pairs


def read_json_to_list_of_dicts():
    """
    Reads a JSON file containing structured data and returns it as a list of dictionaries.

    The JSON file should contain a list of records, where each record is a dictionary
    with keys like 'domain', 'business_requirements', 'technical_requirements', 'question',
    'model_answer', and 'basic_feedback'.

    Parameters:
    file_path (str): The path to the JSON file that needs to be read.

    Returns:
    list: A list of dictionaries, each dictionary representing a data record from the JSON file.

    Example:
    >>> file_path = 'data.json'
    >>> data_records = read_json_to_list_of_dicts(file_path)
    >>> for record in data_records:
    >>>     print(record)
    """

    print("Reading Database of Case Study Objects...")
    # Open and load the JSON file
    with open("CS_usecases.json", "r") as file:
        data_records = json.load(file)

    return data_records


def sample_data_elements(
    json_file_path="CS_usecases.json", domains=None, sample_size=1
):
    """
    Samples data elements from a JSON file, optionally filtered by domain, with a specified sample size per domain.

    Parameters:
    json_file_path (str): Path to the JSON file.
    domains (list, optional): List of domains to consider for sampling. If None, all domains are considered.
    sample_size (int): Number of samples to take per domain.

    Returns:
    list: A list of sampled data elements, sorted by domain.
    """
    try:
        # Load the JSON data
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Filter data by the provided domain list
        filtered_data = [
            record for record in data if domains is None or record["domain"] in domains
        ]

        # Group data by domain
        data_by_domain = {}
        for record in filtered_data:
            domain = record["domain"]
            data_by_domain.setdefault(domain, []).append(record)

        # Sample data elements per domain
        sampled_data = []
        for domain, records in data_by_domain.items():
            sampled_data.extend(random.sample(records, min(sample_size, len(records))))

        # Sort the sampled data by domain
        sampled_data.sort(key=lambda x: x["domain"])

        return sampled_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def sample_data_by_requirements(
    json_file_path="CS_usecases.json",
    business_reqs=None,
    technical_reqs=None,
    sample_size=1,
):
    """
    Samples data elements from a JSON file based on business and technical requirements.

    Parameters:
    json_file_path (str): Path to the JSON file.
    business_reqs (list, optional): List of business requirements to consider for sampling. If None, all are considered.
    technical_reqs (list, optional): List of technical requirements to consider for sampling. If None, all are considered.
    sample_size (int): Number of samples to take.

    Returns:
    list: A list of sampled data elements.
    """
    try:
        # Load the JSON data
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Filter data based on the provided business and technical requirements
        filtered_data = [
            record
            for record in data
            if (
                business_reqs is None
                or any(req in record["business_requirements"] for req in business_reqs)
            )
            and (
                technical_reqs is None
                or any(
                    req in record["technical_requirements"] for req in technical_reqs
                )
            )
        ]

        # Randomly sample the specified number of elements from the filtered data
        sampled_data = random.sample(
            filtered_data, min(sample_size, len(filtered_data))
        )

        return sampled_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def read_behavioural_questions(file_path="Behavioral_Q_A.json"):
    """
    Reads a list of behavioural questions from a JSON file and returns them as a list of dictionaries.

    Each element in the list is a dictionary containing keys such as 'id', 'question', 'response',
    'expected_elements', and 'feedback'.

    Parameters:
    - file_path (str): The path to the JSON file containing the behavioural questions.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, each representing a behavioural question.

    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - json.JSONDecodeError: If the file is not a valid JSON file.
    """

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list.")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        raise ValueError(
            "Failed to decode JSON. Please ensure the file contains valid JSON."
        )
    except ValueError as ve:
        raise ve
