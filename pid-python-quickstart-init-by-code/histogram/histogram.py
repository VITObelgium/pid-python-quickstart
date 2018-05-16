import rasterio
import numpy as np
import datetime
from pidclient import logging_factory
from pidclient.pid_logging.kafka_log import KafkaLogging

def histogram(image_info):
    """Calculates the histogram for a given (single band) image file."""

    """
    Initialize the logging system with kafka configuration and flush the initial log
    """
    kafka_system=KafkaLogging(brokers="epod1.vgt.vito.be:6668,epod17.vgt.vito.be:6668",topic='pid_test2_es' )
    process_log = logging_factory.LoggingFactory(classes=[kafka_system]).get_logger("-","HISTOGRAM",datetime.datetime.now())
    process_log.add_file(str(image_info['file']),'input','eoproduct',str(image_info['geometry'])).proc_started()

    image_file = image_info['file']
    with rasterio.open(image_file) as src:
        band = src.read()

    hist, _ = np.histogram(band, bins=256)
    process_log.proc_stopped(0,"executor has ended without issues")
    return hist
