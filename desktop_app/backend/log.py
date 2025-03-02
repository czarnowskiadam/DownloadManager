import datetime
import os
import traceback
import inspect

def create_logs_files_paths():
    '''
    Creates and returns paths for log files.

    This function ensures that a "logs_files" directory exists in the script's directory.
    It then generates paths for two log files: "log.txt" and "debug_log.log".

    Returns
    -------
    tuple[str, str]
        A tuple containing:
        - log_file_path (str): The path to "log.txt".
        - debug_log_file_path (str): The path to "debug_log.log".
    '''
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(script_path, "logs_files")
    os.makedirs(dir_path, exist_ok=True) # If directory "logs_files" doesn't exist inside "logs" directory, create one
    log_file_path = os.path.join(dir_path, "log.txt")
    debug_log_file_path = os.path.join(dir_path, "debug_log.log")

    return log_file_path, debug_log_file_path


def create_logs_files():
    '''
    Ensures that log files exist by creating them if they do not already exist.

    This function retrieves the log file paths and checks if they exist.
    If a log file does not exist, it is created as an empty file.

    Notes
    -----
    - Uses `open(file, "w").close()` to create an empty file without keeping it open.
    '''
    log_file_path = create_logs_files_paths()[0] 
    debug_log_file_path = create_logs_files_paths()[1] 

    if not os.path.exists(log_file_path):                       
        open(log_file_path, "w").close()

    if not os.path.exists(debug_log_file_path):                       
        open(debug_log_file_path, "w").close()

def clear_logs_files():
    '''
    Clears the contents of the log files without deleting them.

    This function retrieves the log file paths and truncates their contents to 0 bytes,
    effectively clearing the logs while preserving the files.

    If a log file does not exist, it is ignored.

    Notes
    -----
    - Uses `r+` mode to ensure the file is not recreated if it doesn’t exist.
    '''
    log_file_path = create_logs_files_paths()[0]
    debug_log_file_path = create_logs_files_paths()[1] 

    if os.path.exists(log_file_path):
        with open(log_file_path, "r+") as log_file:
            log_file.truncate(0)

    if os.path.exists(debug_log_file_path):
        with open(debug_log_file_path, "r+") as debug_log_file:
            debug_log_file.truncate(0)

def write_log(message: str):
    '''
    Writes a log message to the beginning of the log file.
    
    If the log file exists, the message is prepended to the file, ensuring the newest
    logs appear first. A temporary file is used to avoid corruption during writing.
    If the message is empty, the function does nothing.

    Parameters
    ----------
    message : str
        The log message to be written.
    '''
    log_file_path = create_logs_files_paths()[0]
    temp_path = log_file_path + ".tmp"

    if not os.path.exists(log_file_path):
        return

    if message == '':
        return

    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    complete_message = f'[{time_stamp}]  {message}'
    
    with open(temp_path, "w") as temp_file, open(log_file_path, "r") as log_file:
        temp_file.write(complete_message + "\n")
        for line in log_file:
            temp_file.write(line)
    os.replace(temp_path, log_file_path)

    print(complete_message)

def set_message_to_first_line(log_file_path: str, temp_path: str, error_message: str):
    '''
    Inserts an error message as the first line of a log file.
    
    If the log file exists, the message is written to a temporary file first,
    followed by the original contents of the log file. The temporary file then
    replaces the original log file. If the log file does not exist, it is created
    and the message is written as its first line.

    Parameters
    ----------
    log_file_path : str
        The path to the log file where the message should be inserted.
    temp_path : str
        A temporary file path used for writing before replacing the original log file.
    error_message : str
        The message to be inserted at the beginning of the log file.
    '''
    if os.path.exists(log_file_path):
        with open(temp_path, "w") as temp_file, open(log_file_path, "r") as debug_log_file:
            temp_file.write(error_message)
            for line in debug_log_file:
                temp_file.write(line)

        os.replace(temp_path, log_file_path)
    else:
        with open(log_file_path, "w") as debug_log_file:
            debug_log_file.write(error_message)

def write_debug(message: str=""):
    '''
    Logs debug information, including function details and error messages.

    This function writes debug logs to a dedicated debug log file. If a message is provided, 
    it logs the function name, file name, line number, and the message itself. If no message 
    is provided, it logs details about the most recent exception, including traceback information.

    Parameters
    ----------
    message : str, optional
        Custom debug message to log. If empty, the function logs the most recent exception.
    '''
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    debug_log_file_path = create_logs_files_paths()[1]
    temp_path = debug_log_file_path + ".tmp"

    if message != "":
        caller_frame = inspect.stack()[1]
        filename = caller_frame.filename
        func_name = caller_frame.function
        lineno = caller_frame.lineno

        error_message = f"INFO [{time_stamp}]\n\tFunction name: {func_name}\n\tFunction file: {filename}\n\tLine number: {lineno}\n\tMessage: {message}\n"

        set_message_to_first_line(debug_log_file_path, temp_path, error_message)

        print(error_message)
        
        return

    exc_type, exc_value, exc_traceback = traceback.sys.exc_info()
    tb = traceback.extract_tb(exc_traceback)
    
    if not tb:
        return
    
    filename, lineno, func_name, text = tb[-1]
    error_message = f"ERROR [{time_stamp}]\n\tFunction name: {func_name}\n\tFunction file: {filename}\n\tLine number: {lineno}\n\tCode: {text}\n\tMessage: {exc_value}\n"

    set_message_to_first_line(debug_log_file_path, temp_path, error_message)

    print(error_message)
