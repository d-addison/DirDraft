import logging

def setup_logger():
   # Configure the root logger
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)

   # Create a file handler
   file_handler = logging.FileHandler("dirdraft.log")
   file_handler.setLevel(logging.INFO)

   # Create a console handler
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)

   # Create a formatter and add it to the handlers
   formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
   file_handler.setFormatter(formatter)
   console_handler.setFormatter(formatter)

   # Add the handlers to the root logger
   logger.addHandler(file_handler)
   logger.addHandler(console_handler)

   return file_handler, console_handler