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
from pidclient.logging_factory import LoggingFactory
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
    
    
class DAGWithExtLogging(DAGWithLogging):
    
    def init_operator(self, info, context=None):
        process_log = LoggingFactory(sysinfo=info).get_logger("-", "AIRFLOW", datetime.now())
        return process_log
    
    def on_start_operator(self, process_log, context=None):
        process_log.pid_entry.job_desc="Airflow operator adapted"
        process_log.proc_started()
        return process_log
        
    def on_stop_operator(self, process_log, context=None, result=None):
        if result is None:
            process_log.proc_stopped(0,"operator is ok")
        elif hasattr(result, 'message'):
            process_log.proc_stopped(-1,str(result.message))
        else:
            process_log.proc_stopped(-1,str(result))
    
    def init_workflow(self, info, context=None):
        process_log = LoggingFactory(sysinfo=info).get_logger("-", "AIRFLOW", datetime.now())
        return process_log
    
    def on_start_workflow(self, process_log, context=None):
        process_log.pid_entry.job_desc="Airflow workflow adapted"
        process_log.proc_started()
        return process_log
        
        
    def on_stop_workflow(self, process_log, context=None, result=None):
        if result is None:
            process_log.proc_stopped(0,"workflow is ok")
        elif hasattr(result, 'message'):
            process_log.proc_stopped(-1,str(result.message))
        else:
            process_log.proc_stopped(-1,str(result))
        
dag = DAGWithExtLogging(
    'tutorial_with_class', default_args=default_args, schedule_interval=timedelta(1))

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

dag.log_operator(dag) 