In order to use the Processing Information DataStore facility, some python instructions must be added in :
- the python driver program (see spark.py)
- the python executor program (see histogram/histogram.py)

In this example, additional information has been added to give information on how and where to log information.  That specific information has been added through the use of a configuration file.

# configuration file

The following configuration template can be used to setup the system

	loggers=<list of comma separated logging facilities to use amongst kafka, file, console and elasticsearch >
	[kafka]	
	brokers=<list of comma separated logging facilities to use amongst kafka, file, console and elasticsearch >
	topic= <kafka topic queue to use>
	
	[file]
	filename = <list of comma separated filenames to use for logging>
	
	[elasticsearch]
	hosts =<list of comma separated urls of elasticsearch servers>
	index = <elasticsearch index to use>
	type = <elasticsearch type to use>

Example : file /data/users/Private/MyOwnUSER/pid.conf

	loggers=kafka,console,file,elasticsearch
	[kafka]	
	brokers=epod1.vgt.vito.be:6668,epod17.vgt.vito.be:6668
	topic=pid_test2_es
	[file]
	filename = /tmp/mainfile.log,/tmp/fallback.log
	[elasticsearch]
	hosts = http://es1.vgt.vito.be:9200
	index = anIndex
	type = aType

# Required code adaptation

The following import must be added in the initial program.

	from pidclient import logging_factory
	
As very first lines of the code, the following code should be inserted :

	process_log = logging_factory.LoggingFactory(pidconfigpath="/data/users/Private/MyOwnUSER/pid.conf").get_logger("<product_id>","<product_type>","<product_date>")
    process_log.proc_started()

The first line initializes the system and indicates that a product of type 
<product_type> with the reference <product_id> and the creation date <product_date> shall be created.  The specific logging directive is provided through the use of the pidconfigpath parameter with the configuration filename as arguement.  It is also possible to set up a pidclient.pidconfigpath environment variable instead of using an instruction parameter. 

The second line asks to register the initial information in the DataStore facility.
Specific logging information can be added between those 2 lines, by adapting the content of the process_log object.

The program should end with 

	process_log.proc_stopped(<exit code>,"<exit message>")
	
that should ideally placed in a 'finally' statement.  It shall log the exit code and, the exit message and close the communication layer to the DataStore facility.



