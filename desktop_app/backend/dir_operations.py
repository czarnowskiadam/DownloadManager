import pathlib
import os
import send2trash
import shutil
from datetime import datetime

from backend import log
from backend import utils

def directory_already_exists(directory_path: str):
    '''
    Checks if a directory already exists at the given path.

    Parameters
    ----------
    directory_path : str
        The absolute or relative path to the directory.

    Returns
    -------
    bool
        True if the directory exists, False otherwise.
    '''
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

def is_directory_empty(directory_path: str):
    '''
    Checks if the specified directory is empty.

    Parameters
    ----------
    directory_path : str
        The absolute or relative path to the directory.

    Returns
    -------
    bool
        True if the directory is empty, False otherwise.
    '''
    return not any(pathlib.Path(directory_path).iterdir())

def is_directory_name_the_same(old_direcotry_path: str, new_directory_path: str):
    '''
    Checks if the directory name remains the same after a potential rename or move.

    Parameters
    ----------
    old_directory_path : str
        The original directory path.
    new_directory_path : str
        The new directory path.

    Returns
    -------
    bool
        True if the directory name is the same, False otherwise.
    '''
    return True if old_direcotry_path == new_directory_path else False

def create_directory(parent_path: str, directory_name: str):
    '''
    Creates a new directory within the specified parent path if it does not already exist.

    Parameters
    ----------
    parent_path : str
        The path where the new directory should be created.
    directory_name : str
        The name of the directory to be created.

    Returns
    -------
    pathlib.Path or None
        The path to the created directory if successful, None if an error occurs.
    '''
    try:
        if directory_already_exists(pathlib.Path(parent_path) / directory_name):
            log.write_log(f"Directory '{directory_name}' already exist in '{parent_path}'")
            return

        directory_path = pathlib.Path(parent_path) / directory_name
        directory_path.mkdir(parents=True, exist_ok=True)
        
        log.write_log(f"Directory '{directory_name}' has been created at '{parent_path}'")

        return directory_path
    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while creating directory '{directory_name}'")
        return

def move_directory_to_trash(directory_path: str):
    '''
    Moves the specified directory to the system trash.

    Parameters
    ----------
    directory_path : str
        The path of the directory to be moved to trash.
    '''
    try:
        dir_path = pathlib.Path(directory_path)

        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return
        
        if not is_directory_empty(dir_path):
            log.write_log(f"Directory '{dir_path.name}' contains another files")
            return

        if dir_path.is_dir():
            send2trash.send2trash(dir_path)
            log.write_log(f"Directory '{dir_path.name}' has been moved to trash successfully")
    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while moving directory '{dir_path.name}' to trash")
        return

def remove_directory(directory_path: str):
    '''
    Removes an empty directory.

    Parameters
    ----------
    directory_path : str
        The path of the directory to be removed.
    '''
    try:
        dir_path = pathlib.Path(directory_path)

        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return
        
        if not is_directory_empty(dir_path):
            log.write_log(f"Directory '{dir_path.name}' contains another files")
            return
        
        if dir_path.is_dir():
            dir_path.rmdir()
            log.write_log(f"Directory '{dir_path.name}' has been removed")
    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while removing directory '{dir_path.name}'")
        return
    
def remove_not_empty_directory(directory_path: str):
    '''
    Removes directory that is not empty.

    Parameters
    ----------
    directory_path : str
        The path of the directory to be removed.
    '''
    try:
        dir_path = pathlib.Path(directory_path)

        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return
        
        if dir_path.is_dir():
            shutil.rmtree(dir_path)
            log.write_log(f"Directory '{dir_path.name}' has been removed with all its files")
    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while removing directory '{dir_path.name}'")
        return
    
def rename_directory(directory_path: str, new_directory_name: str):
    '''
    Renames a directory to a new name within the same parent directory.

    Parameters
    ----------
    directory_path : str
        The path to the directory that should be renamed.
    new_directory_name : str
        The new name for the directory.
    '''
    try:
        dir_path = pathlib.Path(directory_path)
        dir_path_name = dir_path.name
        new_dir_path = dir_path.parent / new_directory_name

        if is_directory_name_the_same(dir_path, new_dir_path):
            log.write_log(f"New directory name is the same as old. Nothing happened")
            return
        
        dir_path.rename(new_dir_path)
        log.write_log(f"Directory name '{dir_path_name}' has been changed to '{new_dir_path.name}'")
        

    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while renaming directory '{dir_path.name}'")
        return
    
def move_directory(directory_path: str, new_directory_path):
    '''
    Moves a directory to a new location.

    Parameters
    ----------
    directory_path : str
        The path of the directory to be moved.
    new_directory_path : str
        The destination path where the directory should be moved.
    '''
    try:
        dir_path = pathlib.Path(directory_path)
        new_dir_path = pathlib.Path(new_directory_path)

        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' does not exist and cannot be moved.")
            return

        if directory_already_exists(new_dir_path):
            log.write_log(f"Cannot move directory '{dir_path.name}', because it already exists at the destination '{new_directory_path}'.")
            return
        
        shutil.move(dir_path, new_dir_path)
        log.write_log(f"Directory '{dir_path.name}' has been moved to new localisation")

    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while moving directory '{dir_path.name}'")
        return
    
def get_dictionary_stats(directory_path: str):
    '''
    Retrieves statistics about a specified directory.

    Parameters
    ----------
    directory_path : str
        The path to the directory whose statistics should be gathered.

    Returns
    -------
    dict or None
        A dictionary containing:
        - "name": Directory name
        - "file_count": Number of files inside the directory (including subdirectories)
        - "byte_size": Total size in bytes
        - "size": Human-readable size (e.g., "10.5 MB")
        - "subdirectory_count": Number of directories inside the directory
        - "creation_time": Directory creation time (formatted as YYYY-MM-DD HH:MM:SS)
        
        Returns None if an error occurs.
    '''
    try:
        dir_path = pathlib.Path(directory_path)

        if not dir_path.exists():
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return
        
        if not dir_path.is_dir():
            log.write_log(f"Directory '{dir_path.name}' is not a directory")
            return
        
        files = [file for file in dir_path.rglob("*") if file.is_file()]
        byte_size = sum(file.stat().st_size for file in files)
        subdirectory_count = len([f for f in dir_path.iterdir() if f.is_dir()])
        
        directory_info = {
            "name": dir_path.name,
            "file_count": len(files),
            "byte_size": byte_size,
            "size": utils.format_bytes(byte_size),
            "subdirectory_count": subdirectory_count,
            "creation_time": datetime.fromtimestamp(dir_path.stat().st_birthtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    
        return directory_info
    except Exception:
        log.write_debug()
        log.write_log(f"Error occurred while retrieving stats for directory '{directory_path}'")
        return
    
def set_folder_icon(directory_path: str, icon_path: str):
    '''
    Sets a custom icon for a folder by creating a "desktop.ini" file.

    Parameters
    ----------
    folder_path : str
        Path to the folder where the icon should be set.
    icon_path : str
        Path to the .ico file that will be used as the icon.
    '''
    try:
        dir_path = pathlib.Path(directory_path)
        icon = pathlib.Path(icon_path)

        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return

        if not dir_path.is_dir():
            log.write_log(f"Chosen file '{dir_path.name}' is not a directory")
            return
        
        if not icon.exists():
            log.write_log(f"Chosen icon '{icon.name}' doesn't exists")
            return
        
        if icon.suffix.lower() != ".ico":
            log.write_log(f"Chosen file '{icon.name}' is not an icon file. Needed type of file: '.ico'")
            return
        
        ini_content = f"""[.ShellClassInfo]
                        IconResource={icon},0
                        [ViewState]
                        Mode=
                        Vid=
                        FolderType=Generic"""

        ini_path = dir_path / "desktop.ini"
        with open(ini_path, "w") as ini_file:
            ini_file.write(ini_content)

        os.system(f'attrib +s "{dir_path}"')
        os.system(f'attrib +h "{ini_path}"')

        log.write_log(f"Icon set to directory: '{dir_path.name}'")

    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while setting icon to '{dir_path.name} directory'")

def reset_directory_icon(directory_path: str):
    """
    Resets the folder icon to the default system icon by deleting the desktop.ini file.

    Parameters
    ----------
    directory_path : str
        The path to the folder whose icon should be reset.
    """
    dir_path = pathlib.Path(directory_path)
    desktop_ini = dir_path / "desktop.ini"

    try:
        if not directory_already_exists(dir_path):
            log.write_log(f"Directory '{dir_path.name}' doesn't exists")
            return

        if not dir_path.is_dir():
            log.write_log(f"Chosen file '{dir_path.name}' is not a directory")
            return

        if not desktop_ini.exists():
            log.write_log(f"Directory '{dir_path.name}' already has default icon")
            return
        
        desktop_ini.unlink()

        os.system(f'attrib -s -h "{dir_path}"')

        log.write_log(f"Default icon restored for direcotry '{dir_path.name}'")
    except Exception:
        log.write_debug()
        log.write_log(f"Error occured while setting default icon to '{dir_path.name} directory'")