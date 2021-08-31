""" Simple snowflake DAG """

import logging
from datetime import datetime
import requests

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

args = {"owner": "Airflow", "start_date": airflow.utils.dates.days_ago(2)}

dag = DAG(
    dag_id="snowflake_test", default_args=args, schedule_interval=None
)


def today_in_california():
    url = 'https://covidtracking.com/api/v1/states/ca/' +\
          datetime.today().strftime('%y%m%d') + '.json'
    res = requests.get(url).json()

    print(res)
    print(res.keys())

    positive, negative = res.get('positive', ''), res.get('negative', '')

    return f"insert into TEST_TABLE values('{positive}', '{negative}')"


def get_row_count(**context):
    """ row count """
    dwh_hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    result = dwh_hook.get_first("select count(*) from public.test_table")
    logging.info("Number of rows in `public.test_table`  - %s", result[0])


with dag:
    insert = SnowflakeOperator(
        task_id="snowfalke_create",
        sql=today_in_california(),
        snowflake_conn_id="snowflake_default",
    )

    get_count = PythonOperator(task_id="get_count", python_callable=get_row_count)

insert >> get_count
