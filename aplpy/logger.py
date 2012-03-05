import os
import logging
from ConfigParser import SafeConfigParser

# Read in configuration file
config = SafeConfigParser()
config.read(os.path.expanduser('~/.aplpyrc'))

# Get level from configuration file
if config.has_option('logging', 'level'):
    level = config.getint('logging', 'level')
else:
    level = logging.INFO

# Find out whether to use color logging
if config.has_option('logging', 'color'):
    color = config.getboolean('logging', 'color')
else:
    color = True


def add_coloring_to_emit_ansi(fn):
    def new(*args):
        levelno = args[1].levelno
        if(levelno >= 50):
            color = '\x1b[31m'  # red
        elif(levelno >= 40):
            color = '\x1b[31m'  # red
        elif(levelno >= 30):
            color = '\x1b[33m'  # yellow
        elif(levelno >= 20):
            color = '\x1b[32m'  # green
        elif(levelno >= 10):
            color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'  # normal
        args[1].levelname = color + args[1].levelname + '\x1b[0m'  # normal
        return fn(*args)
    return new

# Initialize logger
logging.basicConfig(format="%(levelname)s: %(message)s", level=level)
logger = logging.getLogger()

if color:
    f = logging.Formatter("%(levelname)s: %(message)s")
    if len(logger.handlers) > 0:
        logger.handlers[0].setFormatter(f)
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
