# gunicorn_config.py

import multiprocessing

def post_fork(server, worker):
    from multiprocessing import util
    util._exit_function = util._original_exit_function

def worker_init(worker):
    from ctypes import CDLL
    import ctypes.util

    # Suppress ALSA error messages
    ctypes.util.find_library('sndfile') or CDLL('libsndfile.so.1', mode=1)

# Gunicorn config
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
reload = True
worker_class = "gevent"
