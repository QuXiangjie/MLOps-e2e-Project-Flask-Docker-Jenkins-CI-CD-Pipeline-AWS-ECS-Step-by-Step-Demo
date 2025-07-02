import pickle
import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Load the model
MODEL_PATH = "/opt/airflow/data/iris_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise Exception(
        "Model file not found. Make sure to train the model by running 'train.py'."
    )

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Provide default values for environment variables if they are not set
host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", 3306))  # Default to 3306 if not set
user = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "")
database = os.getenv("DB_NAME", "test")

# Function to test database connection
def test_database_connection():
    try:
        connection = mysql.connector.connect(
            host=host, port=port, user=user, password=password, database=database
        )

        if connection.is_connected():
            return "Database connection successful!"
    except Error as e:
        return f"Error while connecting to the database: {e}"
    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()

# Streamlit UI
st.title("Iris Prediction and Model Retraining")

# Section: Test Database Connection
st.header("Database Connection")
if st.button("Test Database Connection"):
    db_status = test_database_connection()
    st.write(db_status)


# Section: Predict Iris Class
st.header("Predict Iris Class")
sepal_length = st.text_input("Sepal Length")
sepal_width = st.text_input("Sepal Width")
petal_length = st.text_input("Petal Length")
petal_width = st.text_input("Petal Width")

if st.button("Predict"):
    try:
        features = [
            float(sepal_length),
            float(sepal_width),
            float(petal_length),
            float(petal_width),
        ]
        prediction = model.predict([features])[0]
        st.success(f"Predicted Iris Class: {prediction}")
    except Exception as e:
        st.error(f"Error: {e}")