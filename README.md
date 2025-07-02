# Project Structure

This document provides an overview of the project structure and the purpose of each file and folder.

## Root Directory

### Files
- **`app.py`**
  - Main application file for Streamlit and database logic.
  - Implements the user interface and handles database connections and predictions.

- **`Dockerfile`**
  - Defines the containerization process for the project.
  - Includes steps to install dependencies, train the model, and run the application.

- **`entrypoint.sh`**
  - Entrypoint script for initializing services like Airflow and Streamlit when the container starts.

- **`requirements.txt`**
  - Lists all Python dependencies required for the project.

- **`test_mysql_connection.ipynb`**
  - Jupyter Notebook for testing MySQL database connectivity.
  - Includes steps to load environment variables, connect to the database, and execute queries.

- **`train.py`**
  - Script for training a machine learning model.
  - Saves the trained model to a specified path for later use.

- **`.dockerignore`**
  - Ensures sensitive files like `.env` are excluded from the Docker image.

## Subdirectories

### `dags/`
- Contains Airflow DAGs for orchestrating machine learning pipelines.
- **`ml_pipeline_dag.py`**
  - Defines an Airflow DAG for managing the machine learning pipeline tasks.

---

## Key Features
- **Containerization**: The project is fully containerized using Docker, with a clear `Dockerfile` and `entrypoint.sh`.
- **Task Orchestration**: Airflow is used to manage and schedule machine learning pipeline tasks.
- **Database Integration**: Includes functionality to connect to a MySQL database for data retrieval and processing.
- **Model Training**: A dedicated script (`train.py`) handles model training and saving.
- **Testing**: A Jupyter Notebook (`test_mysql_connection.ipynb`) is provided for testing database connectivity.

---

## Notes
- Ensure the `.env` file is properly configured with database credentials and other environment variables.
- Use the `.dockerignore` file to exclude sensitive files from the Docker image.
- Follow the instructions in the `Dockerfile` and `entrypoint.sh` for building and running the containerized application.