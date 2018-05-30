In order to use the Processing Information DataStore facility for airflow, the dag definition should be replaced by one that extends the DAGWithLogging class (from pidclient.airflow_utils).  

The next section gives details on the approach.  It shall only address the specificities of the airflow system.  Please, refer to the previous examples pid-python-quickstart-* for the usage of the process_log object.

# Extension of DAGWithLogging

The following import must be added in the initial program.

	from pidclient.airflow_utils import DAGWithLogging
	
This shall make a new DAGWithLogging class available to the airflow dag definition.  That class should be extended with 3 methods that indicate how to complete process log information :

	def init_operator(self, info, context=None)
	def on_start_operator(self, process_log, context=None)
	def on_stop_operator(self, process_log, context=None, result=None)

Each of the 3 methods receives a persisted process_log information that can be adapted by the user according the needs.  Those methods can return None, or a new process_log information depending on the needs.  This can be usefull to create a new process_log object within the proc-started method if the one provided doesn't fill the needs (due to an incorrect/incomplete created logging DataStore facility for example).

Example :

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

That new class can then be used to declare the dag.

Example :

	dag = DAGWithExtLogging('tutorial_with_class', default_args=default_args, schedule_interval=timedelta(1))
    

  