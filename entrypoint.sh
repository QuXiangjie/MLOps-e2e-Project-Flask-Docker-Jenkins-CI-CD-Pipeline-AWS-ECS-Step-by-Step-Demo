#!/bin/bash

# Set default Airflow environment variables
export AIRFLOW__WEBSERVER__DEFAULT_USER=admin
export AIRFLOW__WEBSERVER__DEFAULT_PASSWORD=admin
export AIRFLOW__CORE__DAGS_FOLDER=/app/dags

# Initialize Airflow DB (safe to rerun)
airflow db init

# Create admin user if not exists (ignore if already created)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || true

# Start the Airflow scheduler in the background
airflow scheduler &

# ✅ Start Airflow webserver binding to 0.0.0.0:8080 (important!)
airflow webserver --port 8080 --host 0.0.0.0 &

# ✅ Start Streamlit app also binding to 0.0.0.0:8501
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
