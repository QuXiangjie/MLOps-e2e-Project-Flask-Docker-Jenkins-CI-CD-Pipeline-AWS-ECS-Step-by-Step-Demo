# Project Overview for IT Department

## Project Structure

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

### Subdirectories

#### `dags/`
- Contains Airflow DAGs for orchestrating machine learning pipelines.
- **`ml_pipeline_dag.py`**
  - Defines an Airflow DAG for managing the machine learning pipeline tasks.

---

## Tools Used

### **Airflow**
- Used for orchestrating machine learning pipelines.
- DAGs are defined to automate tasks like data cleaning, model training, and predictions.

### **Docker**
- Containerizes the application for consistent deployment.
- The `Dockerfile` ensures all dependencies are installed and the application is ready to run.

### **AWS Services**

#### **ECR (Elastic Container Registry)**
- Stores Docker images for deployment.
- Images are pushed to ECR and pulled by ECS for running tasks.

#### **ECS (Elastic Container Service)**
- Runs containerized tasks and services.
- Used to deploy the application and manage its lifecycle.

#### **S3 (Simple Storage Service)**
- Stores trained machine learning models.
- Models are uploaded to S3 after training and downloaded for predictions.

#### **RDS (Relational Database Service)**
- Two databases are used:
  - **Airflow Database**: Stores Airflow metadata.
  - **Prediction Database**: Stores prediction results.

#### **Secrets Manager**
- Securely stores sensitive information like database credentials.
- Ensures credentials are not hardcoded in the application.

#### **IAM (Identity and Access Management)**
- Manages permissions for AWS resources.
- Roles and policies are assigned to ECS tasks and users.

---

## Deployment Process

### **Step 1: Push Docker Image to ECR**
1. Build the Docker image:
   ```bash
   docker build -t airflow-dags-project .
   ```
2. Tag the image:
   ```bash
   docker tag airflow-dags-project:latest <account-id>.dkr.ecr.<region>.amazonaws.com/airflow-dags-project:latest
   ```
3. Push the image to ECR:
   ```bash
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/airflow-dags-project:latest
   ```

### **Step 2: Deploy to ECS**
1. Create an ECS cluster.
2. Define a task with the ECR image and required environment variables.
3. Attach an IAM role to the task for accessing S3, RDS, and Secrets Manager.
4. Create a service to run the task and ensure high availability.

### **Step 3: Configure S3**
1. Create an S3 bucket for storing models.
2. Attach a policy to the IAM role for accessing the bucket.

### **Step 4: Set Up RDS**
1. Create two RDS instances:
   - One for Airflow metadata.
   - One for storing prediction results.
2. Configure security groups to allow access from ECS tasks.

### **Step 5: Use Secrets Manager**
1. Store database credentials in Secrets Manager.
2. Attach a policy to the IAM role for accessing Secrets Manager.

---

## Request for IT Department

### **User and Role Assignment**
- Assign me a user account in the company’s AWS account.
- Grant the following permissions:
  - **ECR**: Push and pull Docker images.
  - **ECS**: Create and manage tasks and services.
  - **S3**: Read and write access to the model bucket.
  - **RDS**: Access to the Airflow and prediction databases.
  - **Secrets Manager**: Access to stored credentials.

---

Let me know if you need further clarification or adjustments to the deployment process!