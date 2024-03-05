# gunicorn_config.py

def post_fork(server, worker):
    from multiprocessing import util
    util._exit_function = util._original_exit_function

def worker_init(worker):
    from ctypes import CDLL
    import ctypes.util

    # Suppress ALSA error messages
    ctypes.util.find_library('sndfile') or CDLL('libsndfile.so.1', mode=1)

# Disable Gunicorn from trying to access audio devices
def pre_fork(server, worker):
    import soundfile as sf
    import sys
    sys.modules["soundfile"] = sf
