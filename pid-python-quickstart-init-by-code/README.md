In order to use the Processing Information DataStore facility, some python instructions must be added in :
- the python driver program (see spark.py)
- the python executor program (see histogram/histogram.py)

In this example, additional information has been added to give information on how and where to log information.  In this case, the way to log to Kafka has been provided.

# Required adaptation

The following imports must be added in the initial program.

	from pidclient import logging_factory
	from pidclient.pid_logging.kafka_log import KafkaLogging

The following other imports can also be used :

	from pidclient.pid_logging.file_log import FileLogging
	from pidclient.pid_logging.console_log import ConsoleLogging
	from pidclient.pid_logging.elasticsearch_log import ElasticsearchLogging

As very first lines of the code, the following code should be inserted :

	kafka_system=KafkaLogging(brokers="epod-master1.vgt.vito.be:6668,epod-master2.vgt.vito.be:6668,epod-master3.vgt.vito.be:6668",topic='pid_2_es' )
    process_log = logging_factory.LoggingFactory(classes=[kafka_system]).get_logger("-","HISTOGRAM",datetime.now())

The first line initialize the kafka logging object with the required information. The following other logging system could be used :

	file_system=FileLogging(filename="/tmp/log.txt")
	console_system=ConsoleLogging()
	elasticsearch_system=ElasticsearchLogging(hosts="http://es1.vgt.vito.be:9200",index="index",type="product")

The second line initializes the system and indicates that a product of type 
<product_type> with the reference <product_id> and the creation date <product_date> shall be created.  The newly instanciated KafkaLogging logging object has been placed in the array of DataStore facilities to use through the "classes" parameter.

The third line asks to register the initial information in the DataStore facility.
Specific logging information can be added between those 2 lines, by adapting the content of the process_log object.

The program should end with 

	process_log.proc_stopped(<exit code>,"<exit message>")
	
that should ideally placed in a 'finally' statement and before the halt of the spark context.  It shall log the exit code and, the exit message and close the communication layer to the DataStore facility.



