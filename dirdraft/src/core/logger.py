import logging

def setup_logger():
   logger = logging.getLogger("dirdraft")
   logger.setLevel(logging.INFO)

   # Create a file handler
   file_handler = logging.FileHandler("dirdraft.log")
   file_handler.setLevel(logging.INFO)

   # Create a console handler
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)

   # Create a formatter and add it to the handlers
   formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
   file_handler.setFormatter(formatter)
   console_handler.setFormatter(formatter)

   # Add the handlers to the logger
   logger.addHandler(file_handler)
   logger.addHandler(console_handler)

   return logger