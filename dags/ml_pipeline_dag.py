from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import mysql.connector
import os
import time
from mysql.connector import Error

# Fetch DB credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Task 1: Connect to MySQL database and return success
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("✅ Connected to database successfully")
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Task 2: Simulate data cleaning

def clean_data():
    time.sleep(5)
    print("✅ Clean Data step completed")

# Task 3: Simulate model training

def train_model():
    time.sleep(5)
    print("✅ Train Model step completed")

# Task 4: Simulate prediction

def predict():
    time.sleep(5)
    print("✅ Predict step completed")

# Define the DAG
dag = DAG(
    'ml_pipeline_dag',
    default_args=default_args,
    description='A simulated ML pipeline with DB connection',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 6, 30),
    catchup=False
)

# Define tasks
t1 = PythonOperator(
    task_id='connect_to_database',
    python_callable=connect_to_db,
    dag=dag
)

t2 = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag
)

t3 = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

t4 = PythonOperator(
    task_id='predict',
    python_callable=predict,
    dag=dag
)

# Set task dependencies
t1 >> t2 >> t3 >> t4
