from uvicorn.workers import UvicornWorker


class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        'timeout_keep_alive': 5,
        'backlog': 2048,
        'limit_concurrency': 5000,
        'limit_max_requests': 100000
    }