import pickle
import os
from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Load the model
MODEL_PATH = "model/iris_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise Exception(
        "Model file not found. Make sure to train the model by running 'train.py'."
    )

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Function to test database connection
def test_database_connection():
    try:
        # Get database credentials from environment variables
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")

        # Connect to the database
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            return "Database connection successful!"
    except Error as e:
        return f"Error while connecting to the database: {e}"
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Home route to display the form and database connection status
@app.route("/")
def home():
    db_status = test_database_connection()
    return render_template("index.html", db_status=db_status)

# Prediction route to handle form submissions
@app.route("/predict", methods=["POST"])
def predict():
    # Get the input features from the form
    features = [float(x) for x in request.form.values()]

    # Make a prediction using the model
    prediction = model.predict([features])[0]

    # Display the prediction on the same page
    return render_template(
        "index.html", prediction_text=f"Predicted Iris Class: {prediction}"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)