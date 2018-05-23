In order to use the Processing Information DataStore facility for airflow, 2 approaches can be taken :

- the dag definition can be replaced by one that extends the DAGWithLogging class (from pidclient.airflow_utils).  This method can presently be used only for the main workflow.  The steps can't be logged automatically that way.  The user can nevertheless adapt himself the steps to build an use a process_log object.
- the initial dag version can be patched with dedicated methods.  This approach works for both steps and the main worlflow.

The next section gives details on the 2 approaches.  They shall only address the specificities of the airflow system.  Please, refer to the previous examples pid-python-quickstart-* for the usage of the process_log object.

# Extension of DAGWithLogging

The following import must be added in the initial program.

	from pidclient.airflow_utils import DAGWithLogging
	
This shall make a new DAGWithLogging class available to the airflow dag definition.  That class should be extended with 2 methods that indicate how to complete process log information :

	def proc_started(self, process_log)
	def proc_stopped(self, process_log)

Each of the 2 methods receives a persisted process_log information that can be adapted by the user according the needs.  Those methods can return None, or a new process_log information depending on the needs.  This can be usefull to create a new process_log object within the proc-started method if the one provided doesn't fill the needs (due to an incorrect/incomplete created logging DataStore facility for example).

Example :

	class DAGWithExtLogging(DAGWithLogging):
	    def proc_started(self, process_log):
	        process_log.pid_entry.job_desc="Airflow process Adapted"
	        return None
	        
	        
	    def proc_stopped(self, process_log):
	        process_log.pid_entry.job_type="airflow"
	        return None

That new class can then be used to declare the dag.

Example :

	dag = DAGWithExtLogging('tutorial_with_class', default_args=default_args, schedule_interval=timedelta(1))
    
# Patching of the existing dag

The following imports must be added in the initial program.

	from pidclient import logging_factory
	from pidclient.airflow_utils import log_driver, log_steps 

Considering that the dag is defined with a description such as
	
	dag = DAG(
    'tutorial_with_steps', default_args=default_args, schedule_interval=timedelta(1))
    
    
The user should put as last line of its program
	
	log_steps(log_driver(dag,my_proc_start,my_proc_end),my_step_start,my_step_end)

 
with 
- dag being the dag definition
- my_proc_start,my_proc_end ,my_step_start,my_step_end being 4 methods defined by the user with the following signature
	
	def <some_name>(self, process_log):
	
	
Those methods shall receive a process_log information that can be adapted by the user according the needs.  Those methods can return None, or a new process_log information depending on the needs.  

Example :

	def my_proc_start(self, process_log):
	    process_log.pid_entry.job_desc="Airflow Workflow Adapted"
	    return None

Note that it is not mandatory to use log_steps and log_driver together.  Only one of them could be used if only steps information or workflow information is required.
  