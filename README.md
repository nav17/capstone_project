# London Underground Capstone ETL Project

This project comprises of an ETL pipeline which extracts static and live crowding data 
in stations across stations on the London Underground from the TfL API, transforms the raw data 
and loads the processed data into a PostgreSQL database. The data is then ingested and visualised 
on a [Streamlit dashboard]().

Data from the Elizabeth Line has been excluded as it is not currently tracked by the API.

The deployed Streamlit dashboard can be found here:

## Installation

### Prerequisites

Requires Python 3.13 or above

### Setup

To setup this project:

```zsh
pip install -r requirements-setup.txt
pip install -e .
```

Create a `.env` file containing the following:
```python
# API Credentials
APP_KEY= # paste app_key here

# Database Configuration
DB_NAME= # enter your database name
DB_USER= # enter your database user
DB_PASSWORD= # enter your database user's password
DB_HOST= # enter your database hostname
DB_PORT= # enter the port your database is running on
DB_SCHEMA= # enter your database schema name
```
An `app_key` is required by the TfL API to make requests
and can be obtained by registering [here](https://api-portal.tfl.gov.uk/) and subscribing to the product:


PSA: the API home page mentions an `app_id` but that has been depreciated and only an `app_key` is required.

To run (during development):

```zsh
python3 -m scripts.run_etl dev
```

To run tests:

```zsh
pytest
```

To run streamlit app:

```zsh
streamlit run streamlit/main.py
```

### Troubleshooting

If tests don't run

```zsh
pip install psycopg_binary
```

## Overview

### User Stories

- As a commuter, I want to see typical and current crowding levels at my station,
  so that I can avoid peak congestion.
- As a tourist, I want to know which stations are the busiest at different times of the day,
  so that I can have a comfortable travelling experience.
- As a data analyst, I want to see the top 5 busiest stations,
  so that I can gain insights to share.
- As a data engineer, I want to create a full ETL pipeline,
  so that I can gain experience in developing production grade code.

### Resources

Dataset API: https://api.tfl.gov.uk/

### Optimisation

If the dataset grew substantially I would take the following steps to optimise performance:
- Use PySpark instead of Pandas to handle larger datasets
- Index key columns to improve query efficiency
- Cache frequent queries to use for high traffic dashboards which query static data

### Error Handling & Logging

Error handling is implemented using Try Except blocks during API request to manage failures
such as `429` rate limits, network issues or missing data. In cases where a station's data is unavailable
or incomplete, None values are recorded to maintain dataset consistency.
Structured logging was not implemented due to time constraints but it can replace the current print statements
and will implemented in a future update.

### Security & Privacy

API Keys and database credentials are stored in a `.env` file and excluded from git to maintain privacy.
The credentials used on the deployed Streamlit app are stored within Streamlit `st.secrets` functionality


### Deploying to cloud

To deploy this project to cloud I would consider two options; keeping the current setup and
deploying the project as an ETL pipeline, or splitting the ETL logic into AWS Lambda functions
and deploying it serverless. I have outlined the process for each method below:

#### ETL Deployment

- Schedule the job using Apache Airflow inside an EC2 instance
- Use Amazon RDS to host the PostgreSQL database and store raw and processed data
- Monitor using AWS CloudWatch

#### Serverless Deployment

- Use AWS Lambda functions to run each part of the ETL, triggered by events
- Store raw and processed data in Amazon S3 as Parquet instead of CSV
- Use Amazon Athena to query the data if required
- Use AWS Secrets Manager to store credentials

If the Streamlit app required hosting it would be containerised and hosted on AWS Fargate 