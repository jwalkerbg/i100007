# logger.py

# logger_module.py
import logging
from datetime import datetime

TAGNAME = "pymodule"

# Custom Formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{log_time} - {record.name} - {record.levelname} - {record.getMessage()}"
        return log_message

# Custom Logging Handler
class StringHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_messages = []

    def emit(self, record):
        log_entry = self.format(record)
        self.log_messages.append(log_entry)

    def get_logs(self):
        return '\n'.join(self.log_messages)

    def clear_logs(self):
        self.log_messages = []

# Logger Setup
logger = logging.getLogger(TAGNAME)
logger.setLevel(logging.INFO)

# Create the custom formatter and string handler
custom_formatter = CustomFormatter()
string_handler = StringHandler()
string_handler.setFormatter(custom_formatter)

# Console handler (for immediate output)
console_handler = logging.StreamHandler()
console_handler.setFormatter(custom_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
# uncomment if you want application slogger to write to a string too
# logger.addHandler(string_handler)

def getAppLogger() -> logging.Logger:
    return logger

def getAreaLogger(area_tag:str, toString:bool=False) -> logging.Logger:
    if not area_tag or len(area_tag) == 0:
        return None
    lg = logging.getLogger(area_tag)
    lg.setLevel(logging.INFO)
    lg.addHandler(console_handler)
    if toString:
        lg.addHandler(string_handler)

    return lg
