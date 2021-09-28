# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example DAG demonstrating simple Apache Airflow operators."""

from __future__ import print_function
import datetime
from airflow import models
from airflow.operators import bash_operator
from airflow.operators import python_operator

# [START composer_simple_define_dag]
default_dag_args = {
    # The start_date describes when a DAG is valid / can be run. Set this to a
    # fixed point in time rather than dynamically, since it is evaluated every
    # time a DAG is parsed. See:
    # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
    'start_date': datetime.datetime(2021, 9, 17),
}

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
        'dag_benhard',
        schedule_interval='0 1 * * *',
        default_args=default_dag_args) as dag:
        
    def greeting():
        import logging
        logging.info('Hello World!')

    initial_command_1 = bash_operator.BashOperator(
        task_id='get_data_from_postgresql_orders_table',
        bash_command='''export PGPASSWORD=jUDQgm5cLTQvoHd5;psql --set=sslmode=require -h shiftacademy-do-user-7592846-0.b.db.ondigitalocean.com -p 25061 -U doadmin -d shiftacademy -c "\copy (select * from orders where order_date = '{{ yesterday_ds }}') to '/home/airflow/gcs/data/benhard/orders/orders_{{ yesterday_ds }}.csv' CSV HEADER" ''')

    initial_command_2 = bash_operator.BashOperator(
        task_id='get_data_from_postgresql_order_details_table',
        bash_command='''export PGPASSWORD=jUDQgm5cLTQvoHd5;psql --set=sslmode=require -h shiftacademy-do-user-7592846-0.b.db.ondigitalocean.com -p 25061 -U doadmin -d shiftacademy -c "\copy (select * from order_details od where order_id in (select distinct order_id from orders o2 where order_date = '{{ yesterday_ds }}')) to '/home/airflow/gcs/data/benhard/order_details/order_details_{{ yesterday_ds }}.csv' CSV HEADER" ''')

    first_command_1 = bash_operator.BashOperator(
        task_id='move_to_datalake_orders',
        bash_command='gsutil cp gs://us-central1-shifacademy-b6818520-bucket/data/benhard/orders/orders_{{ yesterday_ds }}.csv gs://shiftacademy-final-project/benhard/orders/orders_{{ yesterday_ds }}.csv ')

    first_command_2 = bash_operator.BashOperator(
        task_id='move_to_datalake_order_details',
        bash_command='gsutil cp gs://us-central1-shifacademy-b6818520-bucket/data/benhard/order_details/order_details_{{ yesterday_ds }}.csv gs://shiftacademy-final-project/benhard/order_details/order_details_{{ yesterday_ds }}.csv ')

    second_command_1 = bash_operator.BashOperator(
        task_id='upload_to_bigquery_orders',
        bash_command='bq load --source_format=CSV --skip_leading_rows=1 benhard.orders gs://shiftacademy-final-project/benhard/orders/orders_{{ yesterday_ds }}.csv ')

    second_command_2 = bash_operator.BashOperator(
        task_id='upload_to_bigquery_order_details',
        bash_command='bq load --source_format=CSV --skip_leading_rows=1 benhard.order_details gs://shiftacademy-final-project/benhard/order_details/order_details_{{ yesterday_ds }}.csv ')

    # [END composer_simple_operators]

    # [START composer_simple_relationships]
    # Define the order in which the tasks complete by using the >> and <<
    # operators. In this example, hello_python executes before goodbye_bash.
    initial_command_1 >> first_command_1
    first_command_1 >> second_command_1

    initial_command_2 >> first_command_2
    first_command_2 >> second_command_2

    # [END composer_simple_relationships]
# [END composer_simple]