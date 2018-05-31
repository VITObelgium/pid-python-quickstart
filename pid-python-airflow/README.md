In order to use the Processing Information DataStore facility for airflow, the dag definition should point to a dag that extends the DAGWithLogging class (from pidclient.airflow_utils).  

The next section gives details on the approach.  It shall only address the specificities of the airflow system.  Please, refer to the previous examples pid-python-quickstart-* for the usage of the process_log object.

# Extension of DAGWithLogging

The following import must be added in the initial program :

	from pidclient.airflow_utils import DAGWithLogging
	
This shall provide a new DAGWithLogging class usable as airflow dag definition.  
Nevertheless, in order to be useful as a logging facility, that new class should be extended with 2 groups of 4 methods whose aim is to indicate how to complete process log information :

	init_operator(self, info, context=None)
	on_start_operator(self, process_log, context=None)
	on_operator_success(self, process_log, context=None, result=None)
	on_operator_failure(self, process_log, context=None, received_exception=None)

	init_workflow(self, info, context=None)
	on_start_workflow(self, process_log, context=None)
	on_workflow_success(self, process_log, context=None, result=None)
	on_workflow_failure(self, process_log, context=None, received_exception=None)

The first group deals with operator logging.  The associated methods should be extended only if the user wish to log operation results.  The Second group deals with global workflow logging. 

The aim of 
- the init_* methods is to create a process_log entry from the logging factory, and this according certain configuration parameter.  It is mandatory for such methods to return a process_log entry.
- The on_start_* methods is to indicate to the logging facility that it should start logging information on the process at this point.
- the on_*_success is to provided to the user the result of the call ( if any ) and to let the user log the result ( or any information ) on the step.
- the on_*_failure is to indicate to the user that the call has failed and so that he can log that fact to the logging facility.


Example :

	class DAGWithExtLogging(DAGWithLogging):
    def init_workflow(self, info, context=None):
        process_log = LoggingFactory(sysinfo=info).get_logger("-", "AIRFLOW", datetime.now())
        return process_log
        
    def on_start_workflow(self, process_log, context=None):
        if process_log is not None:
            process_log.proc_started()

    def on_workflow_success(self, process_log, context=None, result=None):
        if process_log is not None:
            if result is None:
                process_log.proc_stopped(0,"")
            else:
                process_log.proc_stopped(0, str(result))

    def on_workflow_failure(self, process_log, context=None, received_exception=None):
        if process_log is not None:
            if received_exception is None:
                process_log.proc_stopped(-1,"Worflow ends with an issue")
            else:
                process_log.proc_stopped(-1, str(received_exception))

That new class can then be used in the dag definition.

Example :

	dag = DAGWithExtLogging('basic_tutorial', default_args=default_args, schedule_interval=timedelta(1))
    

If one wish to log the operator results, it is mandatory to place 

	dag.log_operator(dag) 

as very last line of the dag definition.  That instruction shall indeed adapt the different operators so that they make use of the operator group of methods.
  