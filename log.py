import logging
import os

def create_logger(fn, **kwargs):
    """Create a logger to log to a file and console.

    Give a filename, and optional logging levels (default DEBUG), log to a file.

    KWargs
    - level_file :: logging level (logging.DEBUG etc.)
    - level_console :: as above, but for logging to console."""
    level_file = kwargs.get('level_file', logging.DEBUG)
    level_console = kwargs.get('level_console', logging.DEBUG)
    fmt = '%(asctime)s %(levelname)s -- %(message)s'

    project = os.path.splitext(os.path.basename(fn))[0]
    logger = logging.getLogger(project)
    logger.setLevel(level_file)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(fn)
    fh.setLevel(level_file)

    ch = logging.StreamHandler()
    ch.setLevel(level_console)

    # create formatter and add it to the handlers
    #fmtstr = '%(asctime)s ::: %(levelname)s ::: %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%Y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
