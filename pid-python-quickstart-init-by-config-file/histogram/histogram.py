import rasterio
import numpy as np
import datetime
from pidclient import logging_factory


def histogram(image_info):
    """Calculates the histogram for a given (single band) image file."""

    """
    Initialize the logging system ( which is by default a simple console logger ) and flush the initial log
    """
    process_log = logging_factory.LoggingFactory(pidconfigpath="../pidlogging.conf").get_logger("-","HISTOGRAM",datetime.datetime.now())
    process_log.add_file(str(image_info['file']),'input','eoproduct',str(image_info['geometry'])).proc_started()

    image_file = image_info['file']
    with rasterio.open(image_file) as src:
        band = src.read()

    hist, _ = np.histogram(band, bins=256)
    process_log.proc_stopped(0,"executor has ended without issues")
    return hist
