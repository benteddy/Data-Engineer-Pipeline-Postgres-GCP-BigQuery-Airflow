# Data Engineer Pipeline Project using Postgres - GCP - BigQuery - Airflow
The pipeline is using PostgreSQL as database and Google Cloud Storage as ETL datalake and BigQuery as access datalake. The scheduler is using Airflow.

## Background
My role is as a data engineer to create project for a small retail company. The retail company has a simple postgresql database. The management level wants to create a simple data warehouse and visualization using the google cloud platform and wants the data to be updated every day.

Here is a simple data architecture that needs to be created:

The operational database has been prepared by the backend team. Here is a list of tasks to do:
1. Participants must retrieve data from postgresql and then save it into datalake in the form of csv file in each participant's respective directory.
2. The data in the data lake is loaded to enter the bigquery every day in the participant dataset each.
3. Participants perform script automation to retrieve data from postgresql to datalake (point 1) and from datalake to bigquery (point 2) at 01.00 every day using Apache Airflow (Google Composer) with the previous day's date. For historical data (before today), it is entered into datalake and data  warehouse in bulk (direct).
4. Participants form a simple report:
    - Report revenue per day:

    Gross revenue is the total price for all quantity per product minus the discount. Report is entered in the form of a table with the name dm_daily_gross_revenue.
5. Participants create a visualization using Google Data Studio to display a revenue graph for the past 30 days.

## Prerequisites
These are all libraries you need to install
- print_function
- datetime
- airflow.models
- airflow.operators.bash_operator
- airflow.operators.python_operator

## Getting Started
**Scheduler (Airflow – Google Cloud Composer)**
The schedule script (dag) is stored in the dags folder. An example of a filename with the format is "dag_benhard.py"

Temporary files is stored in the participant's "data>benhard" folder.

**Datalake (Google Cloud Storage)**
Bucket name : shiftacademy-final-project
Directory: <example : benhard>

**Data Warehouse (BigQuery)**
Dataset name : <example : benhard>

**Visualisasi (Google Data Studio)**
Bagikan Link sesuai dengan dashboard visualisasi peserta.
