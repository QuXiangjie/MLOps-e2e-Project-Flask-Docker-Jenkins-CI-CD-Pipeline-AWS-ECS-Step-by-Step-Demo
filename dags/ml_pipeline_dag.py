from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import mysql.connector
from mysql.connector import Error
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

# Constants
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "mlops")

MODEL_PATH = "/opt/airflow/data/iris_model.pkl"
PREDICTIONS_PATH = "/opt/airflow/data/predictions.csv"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'iris_model_pipeline',
    default_args=default_args,
    description='A simple ML pipeline with MySQL',
    schedule_interval=None,
    catchup=False
)

# Task 1: Connect to MySQL
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

# Task 2: Load and prepare data
def clean_data(ti):
    iris = load_iris()
    X = iris.data.tolist()
    y = iris.target.tolist()
    target_names = iris.target_names.tolist()
    ti.xcom_push(key='X', value=X)
    ti.xcom_push(key='y', value=y)
    ti.xcom_push(key='target_names', value=target_names)

# Task 3: Train model
def train_model(ti):
    X = ti.xcom_pull(task_ids='clean_data', key='X')
    y = ti.xcom_pull(task_ids='clean_data', key='y')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    ti.xcom_push(key='X_test', value=X_test)
    ti.xcom_push(key='y_test', value=y_test)

# Task 4: Predict and store to DB
def predict(ti):
    target_names = ti.xcom_pull(task_ids='clean_data', key='target_names')
    X_test = ti.xcom_pull(task_ids='train_model', key='X_test')
    y_test = ti.xcom_pull(task_ids='train_model', key='y_test')
    model = joblib.load(MODEL_PATH)
    y_pred = model.predict(X_test)

    pred_df = pd.DataFrame({
        'Sample': [f"Sample_{i+1}" for i in range(len(X_test))],
        'True_Label': [target_names[y] for y in y_test],
        'Predicted_Label': [target_names[pred] for pred in y_pred]
    })
    pred_df.to_csv(PREDICTIONS_PATH, index=False)
    print(f"✅ Predictions saved to {PREDICTIONS_PATH}")

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sample VARCHAR(255),
                    true_label VARCHAR(255),
                    predicted_label VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            for _, row in pred_df.iterrows():
                cursor.execute("""
                    INSERT INTO predictions (sample, true_label, predicted_label)
                    VALUES (%s, %s, %s)
                """, (row['Sample'], row['True_Label'], row['Predicted_Label']))
            connection.commit()
            print("✅ Predictions written to MySQL")
    except Error as e:
        print(f"❌ Failed to insert predictions: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

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

# Task dependencies
t1 >> t2 >> t3 >> t4
