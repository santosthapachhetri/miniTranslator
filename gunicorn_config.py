# gunicorn_config.py

from multiprocessing import cpu_count
import os

bind = "0.0.0.0:8000"
workers = cpu_count() * 2 + 1
max_requests = 1000
timeout = 30
preload_app = True

def post_fork(server, worker):
    # Reset multiprocessing method to fork for Windows compatibility
    from multiprocessing import set_start_method
    try:
        set_start_method("fork")
    except RuntimeError:
        pass
