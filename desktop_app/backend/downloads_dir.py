import winreg
import pathlib
import ctypes
from datetime import datetime
from collections import Counter

from backend import log
from backend import utils


def get_path_to_downloads_directory():
    '''
    Retrieves the absolute path to the user's "Downloads" folder on Windows.

    This function reads the Windows Registry to obtain the system-defined path to the "Downloads" 
    directory for the current user.

    Returns
    -------
    str
        The absolute path to the "Downloads" folder.
    '''
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders")
    downloads_path, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")

    return downloads_path
    
def is_hidden_or_system_file(filepath: str):
    '''
    Checks if a file is hidden or a system file on Windows.

    Parameters
    ----------
    filepath : str
        The absolute or relative path to the file.

    Returns
    -------
    bool
        True if the file is hidden or a system file, False otherwise.
    '''
    FILE_ATTRIBUTE_HIDDEN = 0x2  # Attribute value of hidden file on WinOS
    FILE_ATTRIBUTE_SYSTEM = 0x4  # Attribute value of system file on WinOS
    attr = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
    return (attr & FILE_ATTRIBUTE_HIDDEN > 0) or (attr & FILE_ATTRIBUTE_SYSTEM > 0)

def get_all_files_path_from_DD():
    '''
    Retrieves a list of all non-hidden and non-system files and directories 
    from the user's "Downloads" folder.

    This function first determines the absolute path to the "Downloads" directory, 
    then iterates through its contents, filtering out hidden and system files.

    Returns
    -------
    list[pathlib.Path]
        A list containing pathlib.Path objects representing the paths of 
        visible files and directories in the "Downloads" folder.
    '''
    download_dir_path = pathlib.Path(get_path_to_downloads_directory())
    
    if download_dir_path is None:
        log.write_debug("Path to Downloads directory has not been found")
        return

    files_paths = []

    for file in download_dir_path.iterdir():
        if not is_hidden_or_system_file(file):
            files_paths.append(file)

    return files_paths

def get_files_info():
    '''
    Retrieves detailed information about all visible files and directories 
    in the user's "Downloads" folder.

    This function gathers metadata such as name, suffix, type, size, creation date, 
    and absolute path for each file or directory in the "Downloads" directory.

    Returns
    -------
    list[dict]
        A list of dictionaries, where each dictionary contains file information:
        - name (str): File or directory name without the suffix.
        - suffix (str): File extension (empty for directories).
        - type (str): "file", "directory", "symlink", or "unknown".
        - size (str): Human-readable file size (e.g., "4.77 MB").
        - byte_size (int): File size in bytes.
        - creation_date (str): File creation date in "YYYY-MM-DD HH:MM:SS" format.
        - path (str): Absolute path to the file or directory.
    '''
    files_paths = get_all_files_path_from_DD()

    if not files_paths:
        log.write_debug("Downloads directory doesn't contain any files")

    files_info = []

    for path in files_paths:
        file_path = pathlib.Path(fr"{path}")

        if file_path.exists():
            if file_path.is_dir():
                file_type = "directory"
            elif file_path.is_file():
                file_type = "file"
            elif file_path.is_symlink():
                file_type = "symlink"
            else:
                file_type = "unknown"

            info = {
                "name": file_path.name.removesuffix(file_path.suffix),
                "suffix": file_path.suffix,
                "type": file_type,               
                "size": utils.format_bytes(file_path.stat().st_size),
                "byte_size": file_path.stat().st_size,
                "creation_date": datetime.fromtimestamp(file_path.stat().st_birthtime).strftime("%Y-%m-%d %H:%M:%S"),
                "path": str(file_path.resolve())
            }
            files_info.append(info)

    return files_info

def get_downloads_dictionary_stats():
    '''
    get_downloads_dictionary_stats _summary_

    Returns
    -------
    _type_
        _description_
    '''
    downloads_dictionary_files_info = get_files_info()

    if not downloads_dictionary_files_info:
        log.write_debug("Downloads directory doesn't contain any files info")
        return

    total_files = len(downloads_dictionary_files_info)

    suffixes_count = dict(Counter(entry['suffix'] for entry in downloads_dictionary_files_info))

    total_size = utils.format_bytes(sum(file["byte_size"] for file in downloads_dictionary_files_info))
    size_per_suffix = dict(Counter(
        {file['suffix']: utils.format_bytes(sum(f['byte_size'] for f in downloads_dictionary_files_info if f['suffix'] == file['suffix'])) for file in downloads_dictionary_files_info}
        ))

    return total_files, suffixes_count, total_size, size_per_suffix
