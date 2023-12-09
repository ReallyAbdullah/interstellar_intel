import pandas as pd
from typing import List
import string


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
