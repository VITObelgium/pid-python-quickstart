This code sample shows how to use the Processing Information DataStore facility to logs information on the execution steps of a computation.  The usage examples are based on the Spark usage sample provided in https://bitbucket.org/vitotap/mep-catalogclient.

Four cases of logging shall be covered :
- The default logging (with no application specific parameters)
- Logging with specific logging directive provided in the python code
- Logging with specific logging directive provided in a configuration file
- Logging with specific logging directive provided in the operating system's environment
- Logging within an airflow environment

The original documentation on how to run the code is still applicable, and reminded here for covenience.

# Development environment setup

PyCharm integration: http://stackoverflow.com/a/34714207/1158374

Note: at least PyCharm Community Edition 2016.2.3 requires that you expand `SPARK_HOME` yourself, so `PYTHONPATH` becomes:

`/path/to/the/spark/directory/python:/path/to/the/spark/directory/python/lib/py4j-some-version.src.zip`

# Running the code
## Locally
Run the `spark.py` script directly in your development environment. This allows for debugging your script.
Run the `run-local` bash script on the command line for a local test run.

Both methods will use the local cpu's of your system. 
## On the Hadoop cluster
### Log into Hadoop
Run `kinit` and provide your MEP password. (Same as VM/portal.)

### Submit your job on Hadoop
Run the `run-cluster` script. It will package your project and submit it to the Hadoop cluster.

Inside this script, you can adjust options such as `--num-executors` to specify the number of parallel executors to use.

Additional Python dependencies as `.zip`, `.egg` or `.py` files can be appended to the `--py-files` argument.

### View job logs Hadoop
As your job now runs on remote servers, the output generated there is not directly visible. You can retrieve the full logs like this:

Find the application ID: it is printed in the console output of the Spark job, for example `application_1484394506558_0055`. Then run:
`yarn logs  -log_files_pattern std.*  -applicationId application_1484394506558_0055`

### Using the Spark UI to inspect the running job
Use X2Go Client to start a remote desktop session with your VM; run Firefox and navigate to the job's tracking URL printed in
Spark's console output, e.g:
[http://epod6.vgt.vito.be:8088/proxy/application_1484394506558_0055](http://epod6.vgt.vito.be:8088/proxy/application_1484394506558_0055).

An overview of the jobs submitted to the cluster is available at
[http://epod6.vgt.vito.be:8088/cluster](http://epod6.vgt.vito.be:8088/cluster).


