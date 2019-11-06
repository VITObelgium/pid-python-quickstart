In order to use the Processing Information DataStore facility, some python instructions must be added in :
- the python driver program (see spark.py)
- the python executor program (see histogram/histogram.py)

In this example, additional information has been added to give information on how and where to log information.  That specific information has been added through the setting of environment variables in the different starting scripts :
- run-cluster.sh
- run-local.sh
- ..

# Required script adaptation
## generalities
The following environment variables can be used as directive for the Processing Information DataStore facility :

	PIDCLIENT_LOGGERS=<list of comma separated logging facilities to use amongst kafka, file, console and elasticsearch >
	PIDCLIENT_KAFKA_BROKERS=<list of comma separated logging facilities to use amongst kafka, file, console and elasticsearch >
	PIDCLIENT_KAFKA_TOPIC= <kafka topic queue to use>
	PIDCLIENT_FILE_FILENAME = <list of comma separated filenames to use for logging>	
	PIDCLIENT_ELASTICSEARCH_HOSTS =<list of comma separated urls of elasticsearch servers>
	PIDCLIENT_ELASTICSEARCH_INDEX = <elasticsearch index to use>
	PIDCLIENT_ELASTICSEARCH_TYPE = <elasticsearch type to use>
	
Nevertheless, for system architecture reason, they can not be simply set through the use of regular bash instruction such as 

	<env variable>=<value> 

they have to be set as configuration directive of the spark-submit command


## run-local
In order to fix the environment variables required to fix the DataStore facility to use, one has to use the classical BASH export instruction before executing the spark-submit command :

	export <env variable>=<value>

Example :

	export PIDCLIENT_LOGGERS=kafka
	export PIDCLIENT_KAFKA_TOPIC=pid_2_es
	export PIDCLIENT_KAFKA_BROKERS=epod-master1.vgt.vito.be:6668,epod-master2.vgt.vito.be:6668,epod-master3.vgt.vito.be:6668

## run-cluster
In order to fix the environment variables required to fix the DataStore facility to use, on have to use the following directive of the spark-submit commands :

	for Executor : --conf spark.executorEnv.<env variable>=<value>
	for Driver : --conf spark.yarn.appMasterEnv.<env variable>=<value>
	
Example :

	--conf spark.executorEnv.pidclient.main.logger=kafka 
	--conf spark.executorEnv.pidclient.kafka.topic=pid_2_es --conf spark.executorEnv.pidclient.kafka.brokers="epod-master1.vgt.vito.be:6668,epod-master2.vgt.vito.be:6668,epod-master3.vgt.vito.be:6668" 
	--conf spark.yarn.appMasterEnv.pidclient.main.logger=kafka 
	--conf spark.yarn.appMasterEnv.pidclient.kafka.topic=pid_2_es 
	--conf spark.yarn.appMasterEnv.pidclient.kafka.brokers="epod-master1.vgt.vito.be:6668,epod-master2.vgt.vito.be:6668,epod-master3.vgt.vito.be:6668"


# Required code adaptation

The following import must be added in the initial program.

	from pidclient import logging_factory
	
As very first lines of the code, the following code should be inserted :

	process_log = logging_factory.LoggingFactory().get_logger("<product_id>","<product_type>","<product_date>")
    process_log.proc_started()

The first line initializes the system and indicates that a product of type 
<product_type> with the reference <product_id> and the creation date <product_date> shall be created.  No specific logging directive are provided.
The second line asks to register the initial information in the DataStore facility.
Specific logging information can be added between those 2 lines, by adapting the content of the process_log object.

The program should end with 

	process_log.proc_stopped(<exit code>,"<exit message>")
	
that should ideally placed in a 'finally' statement and before the halt of the spark context.  It shall log the exit code and, the exit message and close the communication layer to the DataStore facility.



