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
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2017, 6, 1),
}

def print_world():
    print('world')
    return 'This is the world'
    
    
class DAGWithExtLogging(DAGWithLogging):
    
    def init_workflow(self, info, context=None):
        """initiliase the logging factory ( before the workflow is
        executed )

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        process_log = LoggingFactory(sysinfo=info).get_logger("-", "AIRFLOW", datetime.now())
        return process_log
        
    def on_start_workflow(self, process_log, context=None):
        """ fix information in the process_log before the workflow is
        executed

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            process_log.proc_started()
        return process_log

    def on_workflow_success(self, process_log, context=None, result=None):
        """fix information in the process_log after the workflow has
        run successfully

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            if result is None:
                process_log.proc_stopped(0,"")
            else:
                process_log.proc_stopped(0, str(result))

    def on_workflow_failure(self, process_log, context=None, received_exception=None):
        """fix information in the process_log after the workflow has
        failed

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            if received_exception is None:
                process_log.proc_stopped(-1,"Worflow ends with an issue")
            else:
                process_log.proc_stopped(-1, str(received_exception))

    def init_operator(self, info, context=None):
        """initiliase the logging factory ( before the operator is
        executed 

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        process_log = LoggingFactory(sysinfo=info).get_logger("-", "AIRFLOW", datetime.now())
        return process_log
        
    def on_start_operator(self, process_log, context=None):
        """fix information in the process_log before the operator is
        executed

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            process_log.proc_started()
        return process_log

    def on_operator_success(self, process_log, context=None, result=None):
        """fix information in the process_log after the operator has
        run successfully

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            if result is None:
                process_log.proc_stopped(0,"")
            else:
                process_log.proc_stopped(0,str(result))

    def on_operator_failure(self, process_log, context=None, received_exception=None):
        """fix information in the process_log after the operator has
        failed

        :param process_log: the process log
        :type process_log: ProcessLog
        """
        if process_log is not None:
            if received_exception is None:
                process_log.proc_stopped(0,"Operator ends with an issue")
            else:
                process_log.proc_stopped(0, str(received_exception))
        
dag = DAGWithExtLogging(
    'pid_tutorial_spark', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = PythonOperator(
    task_id='print_world',
       python_callable=print_world,
    dag=dag)

t2 = BashOperator(
    task_id='spark_local',
    bash_command='( cd /home/tonneaus/example/python-spark-quickstart ; ./run-local)',
    retries=1,
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