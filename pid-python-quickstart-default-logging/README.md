In order to use the Processing Information DataStore facility, some python instructions must be added in :
- the python driver program (see spark.py)
- the python executor program (see histogram/histogram.py)

Indeed, all the drivers and the executors create their own communication layer, and independently push their information to the DataStore facility.

# Required adaptation

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
	
that should ideally placed in a 'finally' statement.  It shall log the exit code and, the exit message and close the communication layer to the DataStore facility.



