import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s',
                    filename='log.txt',
                    filemode='a')

logger = logging.getLogger('fb_logger')
