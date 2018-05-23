"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pidclient import logging_factory
from pidclient.airflow_utils import DAGWithLogging
from airflow.utils.decorators import apply_defaults
from pidclient.airflow_utils import log_driver, log_steps 
import types

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['stephane.tonneau@nrb.be'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2017, 6, 1),
}

def print_world():
    print('world')

dag = DAG(
    'tutorial_with_steps', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = PythonOperator(
	task_id='print_world',
       python_callable=print_world,
	dag=dag)

t2 = BashOperator(
    task_id='print_env',
    bash_command='/usr/bin/env >/tmp/myenv 2>&1',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)

def print_driver(self, process_log):
    process_log.pid_entry.job_desc="Airflow Workflow Adapted"
    return None

def print_steps(self, process_log):
    process_log.pid_entry.job_desc="Airflow Step adapted"
    return None

log_steps(log_driver(dag,print_driver,print_driver),print_steps,print_steps)