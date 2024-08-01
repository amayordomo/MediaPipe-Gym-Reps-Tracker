import logging
from logging.handlers import RotatingFileHandler

# Define the log format 
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configure the logging
logging.basicConfig(
    filename='app.log',
    filemode='w',  # Overwrite the log file each time
    format=log_format,
    level=logging.DEBUG
)

# Function to get a logger with the current module name
def get_logger(name):
    return logging.getLogger(name)