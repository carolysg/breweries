# Use official image of Apache Airflow
FROM apache/airflow:latest-python3.9

# Change into a root user
USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    openssh-client \
    libpq-dev \
    && apt-get clean

# Change back into a Airflow user
USER airflow

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Define an arg
ARG AIRFLOW_HOME=/opt/airflow

# Copy DAGs to Airflow folder
COPY dags/ /opt/airflow/dags/

# Define work directory
WORKDIR /opt/airflow