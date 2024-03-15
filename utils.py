import os
import sys
from datetime import datetime
import glob
from loguru import logger

def resource_path(*path_parts):
    """Construct a file path from parts."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *path_parts)

def create_directory(path, dir_name=None):
    """Create a directory if it doesn't exist."""
    full_path = os.path.join(path, dir_name) if dir_name else path
    try:
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            logger.info(f"Directory created: {full_path}")
        else:
            logger.info(f"Directory already exists: {full_path}")
    except OSError as error:
        logger.error(f"Error creating directory {full_path}: {error}")
        raise
    return full_path

def setup_loguru_logging():
    logs_path = create_directory(resource_path("logs"))
    log_filename = os.path.join(logs_path, f"log-{datetime.now().strftime('%Y-%m-%d')}.log")
    
    config = {
        "handlers": [
            {"sink": log_filename, "level": "INFO"},
            {"sink": sys.stdout, "level": "INFO"}
        ],
        "extra": {"user": "someone"}
    }
    
    logger.configure(**config)
    logger.info("Logging setup complete with Loguru")
    return logger



def create_file(path, file_name):
    """Create a file if it doesn't exist and return its path.

    Args:
        path (str): The directory path where the file will be created.
        file_name (str): The name of the file to create.

    Returns:
        str: The full path to the created or existing file.
    """
    full_path = os.path.join(path, file_name)
    try:
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as _:
                pass  # Explicitly doing nothing, but file is created/verified.
            logger.info(f"File created: {full_path}")
        else:
            logger.info(f"File already exists: {full_path}")
    except OSError as error:
        logger.error(f"Error creating file {full_path}: {error}")
        raise  # Propagate the exception up to the caller.
    return full_path



def get_files_by_date(source_dir, extensions):
    """Get files sorted by modification date."""
    files = [file for ext in extensions for file in glob.glob(f"{glob.escape(source_dir)}/*.{ext}")]
    files.sort(key=os.path.getmtime)
    return files
