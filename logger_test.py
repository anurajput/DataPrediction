import logging

level = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(level)

# log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# setup file handler
file_handler = logging.FileHandler('hello.log')
file_handler.setLevel(level)

# create a logging format
file_handler.setFormatter(formatter)

# setup stream/console handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(level)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Hello baby')
