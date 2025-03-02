def format_bytes(size) -> str:
    '''
    Converts a file size in bytes to a human-readable format.

    This function iterates through common storage units (B, KB, MB, GB, etc.), 
    converting the given size to the largest possible unit without exceeding 1024.

    Parameters
    ----------
    size : int
        The file size in bytes.

    Returns
    -------
    str
        The formatted file size string with two decimal places and the appropriate unit.
    '''
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    factor = 1024
    for unit in units:
        if size < factor:
            return f"{size:.2f} {unit}"
        size /= factor