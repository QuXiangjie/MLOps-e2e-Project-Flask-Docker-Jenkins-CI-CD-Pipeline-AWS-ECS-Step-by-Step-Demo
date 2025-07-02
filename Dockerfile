# Use a lightweight Python image
FROM python:3.9-slim-bullseye

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    && apt-get clean

# Copy only the requirements file
COPY requirements.txt requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /opt/airflow/data

# Copy the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add a step to run the train.py script to generate the model
RUN python train.py

# Expose Flask, Streamlit, and Airflow ports
EXPOSE 8501 8080

# # Allow passing an environment file during the build process
# ARG ENV_FILE=.env
# COPY $ENV_FILE /app/.env

# # Load environment variables from the file
# RUN export $(cat /app/.env | xargs)

# Command to run the app
# Entrypoint has higher priority than CMD, so we use an entrypoint script to start Airflow and Streamlit
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Use the entrypoint script to start Airflow
ENTRYPOINT ["/entrypoint.sh"]