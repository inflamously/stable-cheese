from logging import INFO, FileHandler, Logger, StreamHandler, getLogger
import os
from sys import stdout


def create_logger():
    logger = getLogger()
    logger.addHandler(StreamHandler(stdout))
    logger.setLevel(INFO)
    return logger
    
    
def register_file_logger(logger: Logger):
    stdout_log_path = os.path.join("logs", "usage.log")
    if not os.path.exists(stdout_log_path): os.mkdir(os.path.dirname(stdout_log_path));
    logger.addHandler(FileHandler(stdout_log_path))