import logging
import sys

# Setup Logging
def get_logger():
    logger = logging.getLogger('ada-play')
    hdlr = logging.FileHandler('/tmp/ada-play.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    sys_hdlr = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    sys_hdlr.setFormatter(formatter)
    logger.addHandler(sys_hdlr)
    logger.setLevel(logging.DEBUG)
    logger.info("DEBUG log level")
    logger.info("Starting AdaPlay...")
    return logger
