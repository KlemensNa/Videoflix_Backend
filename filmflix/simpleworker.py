# custom_worker.py
from rq_win.worker import WindowsWorker
from django_rq import get_queue

# Get the default queue
queue = get_queue('default')

# Create a worker
worker = WindowsWorker([queue])

# Start the worker
worker.work()