import multiprocessing
import os
from ctypes import CDLL
import ctypes.util

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

# Set the AUDIODRIVER environment variable to "none"
env = {
    "AUDIODRIVER": "none",
}

# If you have other environment variables, you can add them here
# env["ANOTHER_VARIABLE"] = "value"

# If you need to set additional Gunicorn configurations, you can do so here
# For example:
# timeout = 120
# loglevel = "info"
# accesslog = "/path/to/access.log"

# Set the working directory to the location of your app module
# Change "/path/to/your/app" to the actual path where your app module is located
# This ensures that Gunicorn can find your app module
chdir = "D:\P\Translator\pythonProject"

# Specify the path to your app module
# Change "app:app" to the actual entry point of your Flask app
module = "app:app"

# Suppress ALSA error messages
ctypes.util.find_library('sndfile') or CDLL('libsndfile.so.1', mode=1)

def post_fork(server, worker):
    from multiprocessing import util
    util._exit_function = util._original_exit_function

def worker_init(worker):
    # Suppress ALSA error messages
    ctypes.util.find_library('sndfile') or CDLL('libsndfile.so.1', mode=1)
