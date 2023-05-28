import multiprocessing
import os

workers_per_core_str = os.environ.get('WORKERS_PER_CORE', '3')
host = '0.0.0.0'
port = '8000'
use_loglevel = 'critical'
use_bind = f'{host}:{port}'

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
web_concurrency = max(int(default_web_concurrency), 2)

accesslog_var = os.getenv('ACCESS_LOG', '-')
use_accesslog = accesslog_var or None
errorlog_var = os.getenv('ERROR_LOG', '-')
use_errorlog = errorlog_var or None
graceful_timeout_str = '120'
timeout_str = '120'
keepalive_str = '5'

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
errorlog = use_errorlog
worker_tmp_dir = '/dev/shm'
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)