# Data Engineer Pipeline Project using Postgres - GCP - BigQuery - Airflow
The pipeline is using PostgreSQL as database and Google Cloud Storage as ETL datalake and BigQuery as access datalake. The scheduler is using Airflow.<br/><br/>

## Background
My role is as a data engineer to create project for a small retail company. The retail company has a simple postgresql database. The management level wants to create a simple data warehouse and visualization using the google cloud platform and wants the data to be updated every day.

Here is a simple data architecture that needs to be created:<br/><br/>
<img src="Data Architecture.png" width="700" height="280"><br/><br/>
The operational database has been prepared by the backend team. Here is a list of tasks to do:
1. Retrieve data from postgresql and then save it into datalake in the form of csv file.
2. The data in the data lake is loaded to enter the bigquery every day in the dataset.
3. Perform script automation to retrieve data from postgresql to datalake (point 1) and from datalake to bigquery (point 2) at 01.00 every day using Apache Airflow (Google Composer) with the previous day's date. For historical data (before today), it is entered into datalake and data  warehouse in bulk (direct).
4. Form a simple report:
    - Report revenue per day:<br/>
    <img src="Report Revenue per Day.png" width="500" height="38"><br/>
    Gross revenue is the total price for all quantity per product minus the discount. Report is entered in the form of a table with the name dm_daily_gross_revenue. Here is the table schema used to this project from the postgres database.<br/>
    <img src="Database Schema.png" width="400" height="310"><br/><br/>
5. Create a visualization using Google Data Studio to display a revenue graph for the past 30 days.

## Prerequisites
These are all libraries you need to install
- print_function
- datetime
- airflow

## Getting Started
### Scheduler (Airflow – Google Cloud Composer)
- **DAG Folder**<br/>
The schedule script (dag) is stored in the dags folder. An example of a filename with the format is "Airflow DAG.py"<br/>
<img src="DAG File Repository.png" width="400" height="155"><br/><br/>
Here is the DAG script for Airflow process.<br/>`Airflow DAG.py`<br/><br/>
- **Airflow Process**<br/>
This is the "Tree View" of DAG.<br/>
<img src="Airflow Process.png" width="850" height="355"><br/><br/>
- **Temporary File**<br/>
Temporary files from postgres database is stored in the "data>benhard" folder.<br/>
<img src="Temporary File.png" width="420" height="150"><br/><br/>
- **Datalake (Google Cloud Storage)**<br/>
The files from temporary is stored in the "benhard" directory.<br/>
Bucket name :               -final-project<br/>
Directory : "benhard"<br/>
<img src="Datalake (Google Data Storage).png" width="650" height="155"><br/><br/>
- **Data Warehouse (BigQuery)**<br/>
The file from Google Cloud Storage is loaded to datalake in BigQuery.<br/>
Dataset name : "benhard"<br/>
<img src="Data Warehouse (BigQuery).png" width="245" height="50"><br/><br/>
### Visualisasi (Google Data Studio)
Data visualization is created from dataset in BigQuery
<img src="Data Visualization (Google Data Studio).png" width="650" height="450"><br/><br/>
