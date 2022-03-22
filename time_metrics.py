from time import perf_counter_ns
from functools import update_wrapper
from collections import deque

from eval_equal import eval_equal,\
                       eval_equal_backtracking,\
                       eval_equal_branch_and_bound

from tests import range_9_0,\
                  range_1_9,\
                  predefined_ops

equal = 200


def timeit(func):
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()

        func(*args, **kwargs)

        duration = perf_counter_ns() - start

        return duration

    update_wrapper(wrapper, func)
    return wrapper


def str_time_ms(time_ns: int):
    return f"{time_ns / 1e6}ms"


def print_summary(summary: dict):
    for method, measure in summary.items():
        print(f"{method}:", str_time_ms(measure), end='\n\n')


@timeit
def measure_bruteforce():
    eval_equal(range_9_0, predefined_ops, equal)


@timeit
def measure_bruteforce_next():
    next(eval_equal(range_9_0, predefined_ops, equal))


@timeit
def measure_consuming_bruteforce():
    gen = eval_equal(range_9_0, predefined_ops, equal)
    deque(gen, maxlen=0)


@timeit
def measure_backtracking():
    eval_equal_backtracking(range_9_0, predefined_ops, equal)


@timeit
def measure_backtracking_next():
    next(eval_equal_backtracking(range_9_0, predefined_ops, equal))


@timeit
def measure_consuming_backtracking():
    gen = eval_equal_backtracking(range_9_0, predefined_ops, equal)
    deque(gen, maxlen=0)


@timeit
def measure_branch_and_bound():
    eval_equal_branch_and_bound(reversed(range_1_9), 45)


def __main():
    summary = {
        "bruteforce": measure_bruteforce(),
        "bruteforce next": measure_bruteforce_next(),
        "bruteforce consuming": measure_consuming_bruteforce(),
        "backtracking": measure_backtracking(),
        "backtracking next": measure_backtracking_next(),
        "backtracking consuming": measure_consuming_backtracking(),
        "branch-and-bound": measure_branch_and_bound()
    }

    print_summary(summary)


if __name__ == "__main__":
    __main()
