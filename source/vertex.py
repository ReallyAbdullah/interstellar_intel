from vertexai.preview.language_models import TextGenerationModel
import vertexai
import os
from typing import Any
from google.cloud import aiplatform

PROJECT_ID = "rex-assistant-407413"
REGION = "europe-west4"


def init_sample(project_id: str, location: str) -> None:
    """
    Initializes the AI Platform client with the given project ID and location.

    Parameters:
    project_id (str): The Google Cloud project ID.
    location (str): The location for the AI Platform resources.
    """
    aiplatform.init(project=project_id, location=location)
    vertexai.init(project=PROJECT_ID, location=LOCATION)


def get_model() -> TextGenerationModel:
    """
    Retrieves the Text Generation Model from AI Platform.

    Returns:
    TextGenerationModel: An instance of the Text Generation Model.
    """
    generation_model = TextGenerationModel.from_pretrained("text-bison@001")
    return generation_model


def get_text_generation(prompt: str = "") -> str:
    """
    Generates text based on a given prompt and additional parameters.

    Parameters:
    prompt (str): The input prompt for text generation.

    Returns:
    str: The generated text response.
    """
    generation_model = get_model()
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40,
    }
    response = generation_model.predict(prompt=prompt, **parameters)

    return response.text
