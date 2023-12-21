# Use an official Python runtime as a parent image
FROM python:3.10.13

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY rex-assistant-407413-c97f23a49575.json ./service_account_key.json

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wkhtmltopdf

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=./service_account_key.json

# Run streamlit when the container launches
CMD ["streamlit", "run", "main.py"]
