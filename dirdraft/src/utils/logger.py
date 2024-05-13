import logging

def setup_logger():
   # Create a file handler
   file_handler = logging.FileHandler("dirdraft.log")
   file_handler.setLevel(logging.INFO)

   # Create a console handler
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)

   return file_handler, console_handler