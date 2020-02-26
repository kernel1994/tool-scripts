import time
import datetime
import functools
from multiprocessing.dummy import Process

import schedule


def _fnow(fmt: str=None):
    if not fmt:
        fmt = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.today().strftime(fmt)


def run_threaded(job_func):
    p = Process(target=job_func, args=('Continue 3 seconds...',))
    p.start()
    # p.join()  # p.join() 将会阻塞，直到调用 join() 方法的进程终止


# This decorator can be applied to
def with_logging(func):
    # 如果不使用这个装饰器工厂函数 @functools.wraps()，
    # 则 example() 函数的名称 example.__name__ 将变为 'wrapper'，
    # 并且 example() 原本的文档字符串 example.__doc__ 将会丢失。
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'LOG: {_fnow()} Running job "{func.__name__}"')
        result = func(*args, **kwargs)
        print(f'LOG: {_fnow()} Job "{func.__name__}" completed\n')
        return result
    return wrapper

@with_logging
def action_3s(s):
    print(f'RUN: {_fnow()} {s}')
    time.sleep(3)


if __name__ == '__main__':
    schedule.every(10).seconds.do(run_threaded, action_3s)

    # for first time
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
