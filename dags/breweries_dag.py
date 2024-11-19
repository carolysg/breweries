from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

db_config = {
    'database': os.getenv("AIRFLOW__CORE__PSYCOPG2_DB"),
    'user': os.getenv("AIRFLOW__CORE__PSYCOPG2_USER"),
    'password': os.getenv("AIRFLOW__CORE__PSYCOPG2_PASS"),
    'host': os.getenv("AIRFLOW__CORE__PSYCOPG2_HOST"),
    'port': os.getenv("AIRFLOW__CORE__PSYCOPG2_PORT"),
}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def create_dirs():
    os.makedirs('./data/bronze', exist_ok=True)
    os.makedirs('./data/silver', exist_ok=True)
    os.makedirs('./data/gold', exist_ok=True)

def extract_brewery_data():
    create_dirs()
    try:
        response_total = requests.get("https://api.openbrewerydb.org/breweries/meta")
        total = int(response_total.json()['total'])
        per_page = 200
        num_page = int(np.ceil(total / per_page))
        df = pd.DataFrame()
        for page in range(num_page):
            params = {
                "page": page + 1,
                "per_page": per_page
            }
            response = requests.get("https://api.openbrewerydb.org/breweries", params=params)
            response.raise_for_status()
            data = response.json()
            df_sample = pd.DataFrame(data)
            df = pd.concat([df, df_sample], ignore_index=True)
        df.to_json('./data/bronze/breweries_raw.json', orient='records')
        logging.info("Brewery data extracted successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error extracting data: {e}")
        raise

def transform_data():
    try:
        df = pd.read_json('./data/bronze/breweries_raw.json')
        df.dropna(axis=1, how='all', inplace=True)
        df['longitude'] = df['longitude'].astype(float)
        df['latitude'] = df['latitude'].astype(float)
        df_final = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
        if df_final['state_province'].equals(df_final['state']):
            df_final.drop('state', axis=1, inplace=True)
        df_final.to_parquet('./data/silver/breweries_transformed.parquet', 
                             partition_cols=['country', 'state_province'], 
                             existing_data_behavior='delete_matching')
        logging.info("Data transformed successfully.")
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        raise

def aggregate_data():
    try:
        df = pd.read_parquet('./data/silver/breweries_transformed.parquet')
        df_grouped = df.groupby(['state_province', 'brewery_type']).size().reset_index(name='brewery_count')
        df_grouped = df_grouped[df_grouped['brewery_count'] > 0]
        df_grouped.to_parquet('./data/gold/brewery_aggregated_state_province.parquet')
        logging.info("Data aggregated successfully.")
    except Exception as e:
        logging.error(f"Error aggregating data: {e}")
        raise

def create_breweries_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS breweries (
                state_province VARCHAR(100),
                brewery_type VARCHAR(100),
                brewery_count INTEGER
            );
        """)

def load_to_postgres():
    try:
        df = pd.read_parquet('./data/gold/brewery_aggregated_state_province.parquet')
        with psycopg2.connect(**db_config) as conn:
            create_breweries_table(conn)
            with conn.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE breweries;")
                execute_values(
                    cur=cursor,
                    sql="""
                        INSERT INTO breweries
                        (state_province, brewery_type, brewery_count)
                        VALUES %s;
                    """,
                    argslist=df.to_dict(orient="records"),
                    template="""
                        (%(state_province)s, %(brewery_type)s, %(brewery_count)s)
                    """
                )
        logging.info("Data loaded into PostgreSQL successfully.")
    except Exception as e:
        logging.error(f"Error loading data into PostgreSQL: {e}")
        raise

with DAG('brewery_pipeline', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_brewery_data
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    aggregate_task = PythonOperator(
        task_id='aggregate_data',
        python_callable=aggregate_data
    )

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    extract_task >> transform_task >> aggregate_task >> load_task