import logging


def create_logger(fn, project, flevel=logging.DEBUG, clevel=logging.DEBUG):
    """Create a logger to log to a file.

    Give a filename and projectname, to get a logger object with the
    specified logging levels."""
    logger = logging.getLogger(project)
    logger.setLevel(flevel)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(fn)
    fh.setLevel(flevel)

    ch = logging.StreamHandler()
    ch.setLevel(clevel)

    # create formatter and add it to the handlers
    fmtstr = '%(asctime)s ::: %(levelname)s ::: %(message)s'
    formatter = logging.Formatter(fmtstr,
                                  datefmt='%Y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
