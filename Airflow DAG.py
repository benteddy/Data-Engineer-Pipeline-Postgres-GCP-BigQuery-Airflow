from __future__ import print_function
import datetime
from airflow import models
from airflow.operators import bash_operator
from airflow.operators import python_operator

default_dag_args = {
    'start_date': datetime.datetime(2021, 9, 17),
}

with models.DAG(
        'dag_benhard',
        schedule_interval='0 1 * * *',
        default_args=default_dag_args) as dag:
        
    def greeting():
        import logging
        logging.info('Hello World!')

    initial_command_1 = bash_operator.BashOperator(
        task_id='get_data_from_postgresql_orders_table',
        bash_command='''export PGPASSWORD=jUDQgm5cLTQvoHd5;psql --set=sslmode=require -h academy-do-user-7592846-0.b.db.ondigitalocean.com -p 25061 -U doadmin -d academy -c "\copy (select * from orders where order_date = '{{ yesterday_ds }}') to '/home/airflow/gcs/data/benhard/orders/orders_{{ yesterday_ds }}.csv' CSV HEADER" ''')

    initial_command_2 = bash_operator.BashOperator(
        task_id='get_data_from_postgresql_order_details_table',
        bash_command='''export PGPASSWORD=jUDQgm5cLTQvoHd5;psql --set=sslmode=require -h academy-do-user-7592846-0.b.db.ondigitalocean.com -p 25061 -U doadmin -d academy -c "\copy (select * from order_details od where order_id in (select distinct order_id from orders o2 where order_date = '{{ yesterday_ds }}')) to '/home/airflow/gcs/data/benhard/order_details/order_details_{{ yesterday_ds }}.csv' CSV HEADER" ''')

    first_command_1 = bash_operator.BashOperator(
        task_id='move_to_datalake_orders',
        bash_command='gsutil cp gs://us-central1-academy-b6818520-bucket/data/benhard/orders/orders_{{ yesterday_ds }}.csv gs://academy-final-project/benhard/orders/orders_{{ yesterday_ds }}.csv ')

    first_command_2 = bash_operator.BashOperator(
        task_id='move_to_datalake_order_details',
        bash_command='gsutil cp gs://us-central1-academy-b6818520-bucket/data/benhard/order_details/order_details_{{ yesterday_ds }}.csv gs://academy-final-project/benhard/order_details/order_details_{{ yesterday_ds }}.csv ')

    second_command_1 = bash_operator.BashOperator(
        task_id='upload_to_bigquery_orders',
        bash_command='bq load --source_format=CSV --skip_leading_rows=1 benhard.orders gs://academy-final-project/benhard/orders/orders_{{ yesterday_ds }}.csv ')

    second_command_2 = bash_operator.BashOperator(
        task_id='upload_to_bigquery_order_details',
        bash_command='bq load --source_format=CSV --skip_leading_rows=1 benhard.order_details gs://academy-final-project/benhard/order_details/order_details_{{ yesterday_ds }}.csv ')

    initial_command_1 >> first_command_1
    first_command_1 >> second_command_1

    initial_command_2 >> first_command_2
    first_command_2 >> second_command_2