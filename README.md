# Breweries Project

# Summary
- [Description](#description)
- [Project Structure](#project-structure)
- [Instructions](#instructions)

<br>

## Description

The Breweries Project is an pipeline designed to extract, process and store brewery data from an external API. The project utilizes Apache Airflow to orchestrate the data pipeline, ensuring that each step is executed in a reliable and repeatable manner.

Tools:
- VSCode: Code editor used for development.
- Git/GitHub: Version control and collaboration.
- Docker: Containerization for consistent environments.
- Postgres: Relational database to persist the aggregated data.
- Airflow: Workflow management tool for scheduling and monitoring the ETL process.
- Python 3.9: Programming language used for the development.

<br>

## Project Structure

The project consists on the following pipeline:

![Pipeline of this project](images/01_pipeline.png)

The ETL process begins by extracting data from an external API, storing it in three stages (bronze, silver, and gold), and finally loading it into a PostgreSQL database. Apache Airflow orchestrates the entire pipeline, managing the flow from extraction to transformation and loading.
- API: The data is fetched from an external source using requests in a Python script.
- Bronze: Raw data is saved in JSON format. More details [here](docs/bronze_data.md).
- Silver: Transformed data is stored. More details [here](docs/silver_data.md).
- Gold: Aggregated and final data is stored here. It's an aggregated table with the quantity of breweries per type and location. More details [here](docs/gold_data.md).
- Postgres: The aggregated data is loaded into the PostgreSQL database for further use. More details [here](docs/postgres_data.md).

The project structure is organized as follows:

```python
breweries/
├── dags/                      # Airflow DAG files
│   └── brewery_pipeline.py     # Main ETL DAG
├── data/                      # Data lake architecture
│   ├── bronze/                 # Raw data storage
│   ├── silver/                 # Transformed data storage
│   └── gold/                   # Aggregated data storage
├── docs/                      # Extra documentations about the data
├── images/                    # Images used on readme
├── logs/                      # Logs for task executions in Airflow
├── scripts/                   # Scripts for Airflow setup
│   └── airflow-entrypoint.sh   # Entrypoint script for Airflow
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables for database configuration
├── Dockerfile                 # Dockerfile for Airflow and dependencies
├── docker-compose.yml         # Docker Compose configuration for services
└── README.md                  # Project documentation
```

<br>

## Instructions

In this section, you'll find all the instructions you need to reproduce this project on your own machine.

### Dependencies

Before running the project, ensure you have the following installed:
- Docker: If you want to run Airflow and Postgres in containers.
- Docker Compose: To manage multi-container applications.

You can install the required Python dependencies using pip (if running outside Docker):
```pip install -r requirements.txt```

### Step-by-step

1. Fork and clone the repository: On the GitHub page of the repository, click on the "Fork" button in the upper right corner to create your own copy of the project. Then, clone your forked repository:
```
git clone https://github.com/<your_username>/breweries_project.git
cd breweries_project
```

2. 