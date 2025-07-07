# Project Structure Diagram

The core of this test project is the use of **Apache Airflow**, an open-source workflow orchestration platform, to automate the entire machine learning pipeline — from data collection and cleaning, to training and prediction — on a scheduled basis. The project is fully deployed through **Docker → ECR → ECS**, with **S3** used for storing trained models and **RDS** for storing both Airflow metadata and prediction results. Additionally, **Streamlit** is integrated as a lightweight frontend tool for testing RDS connectivity and validating model predictions through a user-friendly interface.
![alt text](Pictures/image-system-1.png)
![alt text](Pictures/image-system-2.png)



```
Machine Learning Engineering Project in Pitsco: Airflow-Flask-Docker-AWS-ECS-S3 and RDS
├── (4)app.py                # Main application file for Streamlit front End
├── (1)Dockerfile            # Dockerfile for containerizing the project
├── (3)entrypoint.sh         # Entrypoint script for initializing Airflow and Streamlit
├── README.md             # Project documentation
├── (2)requirements.txt      # Python dependencies for the project in the Dockerfile
├── (Test Purpose)test_mysql_connection.ipynb  # Jupyter Notebook for testing MySQL database connection
├── (1)train.py              # Test script for training the machine learning model
├── (5)dags/                 # Folder containing Airflow DAGs
│   └── ml_pipeline_dag.py  # Airflow DAG for the machine learning pipeline
```

This structure outlines the project organization and the purpose of each file and folder.

---

## Request for IT Department

### **User and Role Assignment**
- Assign me a user account within the company’s AWS account.
- Grant the following permissions:

  - **ECR**: Permission to push and pull Docker images.
  - **ECS**: Permission to create and manage tasks and services.  
    _Recommended policy_: `AmazonECSTaskExecutionRolePolicy`  
    ![ECS Permission](Pictures/image-ECS.png)

  - **S3**: Read and write access to the model storage bucket.  
    _Recommended policy_: `AmazonS3FullAccess`  
    ![S3 Access](Pictures/image-1.png)

  - **RDS**: Access to both the Airflow metadata database and the prediction results database.  
    _Credential management recommendation_: Use **Secrets Manager** (with a customer-managed inline policy).  

    1. This is applicable if the project stores database credentials in Secrets Manager.  
    2. The database user must have permission to:
       - Create two tables (for prediction results and Airflow metadata).
       - Read existing tables from the database (for training data collection).  
       ![RDS Permissions](Pictures/image-2.png)

    3. The RDS security group should:
       - Allow inbound access from the **same security group** (for ECS service communication).
       - Optionally allow inbound access on port **80** from `0.0.0.0/0` for external access to Streamlit (mapped to port `8501`).
       - Allow ports **8080** and **8501** to be accessed by the same security group (internal ECS networking).
       - Temporarily open **ports 8080 and 3306** to `0.0.0.0/0` for browser-based testing (not recommended for production).  
       ![Security Group Settings](Pictures/image-3.png)


  
---

## Data Flow and Execution Overview

### (0) Deployment Phase - (0,1,2,3,4)

- The **Dockerfile** exposes two ports:
  - `8501` for the Streamlit frontend (used for database testing and model prediction).
  - `8080` for the Airflow Web UI (used for DAG monitoring and administration).
  - A sample model is trained using `train.py` during the Docker build phase, ensuring Streamlit can load a model on first launch unitl the Airflow DAG Execution.
- It installs all Python dependencies via `requirements.txt`.
- The container entrypoint (`entrypoint.sh`) is triggered to start both Airflow and Streamlit.
- `app.py` is the configuration file for Streamlit to set up Database Connection and Model Functionality testing

### (1) Airflow DAG Execution (`ml_pipeline_dag.py`) - (5)

The DAG is scheduled to run **every 2 minutes** for testing. It automates the following tasks:

- **Task 1: Connect to Database**
  - Establishes a connection to an RDS MySQL instance using environment variables.
  - Simulates access to real-world PA (proposal analytics) data.

- **Task 2: Clean Data**
  - Preprocesses the Iris dataset.
  - Does not rely on external data sources, ensuring isolated operation.

- **Task 3: Train Model**
  - Trains a logistic regression model.
  - Uploads the serialized `.pkl` model to an S3 bucket for persistent storage and reuse.

- **Task 4: Predict**
  - Loads the model and performs predictions.
  - Writes results into the same RDS database into a new table called `predictions`.

This design enables **Power BI** to automatically refresh and visualize prediction results by connecting directly to the RDS MySQL database, eliminating the need for additional gateways or configurations.

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
