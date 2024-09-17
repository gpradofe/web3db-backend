import multiprocessing

bind = "0.0.0.0:3001"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
timeout = 120
keepalive = 5
reload = True