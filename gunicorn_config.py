# gunicorn.config.py

import multiprocessing

bind = "0.0.0.0:8000"  # Set the host and port
workers = multiprocessing.cpu_count() * 2 + 1  # Adjust the number of workers based on your needs
reload = True
preload_app = True
# Enable automatic reloading on code changes during development
worker_class = "gevent"  # Use the gevent worker class for better performance

# Optional Gunicorn settings
# timeout = 30
# loglevel = "info"
# accesslog = "-"  # Log to stdout

d# gunicorn_config.py

def post_fork(server, worker):
    from multiprocessing import util
    util._exit_function = util._original_exit_function

def worker_init(worker):
    from ctypes import CDLL
    import ctypes.util

    # Suppress ALSA error messages
    ctypes.util.find_library('sndfile') or CDLL('libsndfile.so.1', mode=1)
