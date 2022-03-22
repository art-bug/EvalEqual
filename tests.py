from itertools import chain, starmap

import pytest

from eval_equal import eval_equal,\
                       eval_equal_backtracking,\
                       eval_equal_branch_and_bound

predefined_ops = ('+', '-', '')

range_9_0 = list(reversed(range(9 + 1)))
range_1_9 = list(range(1, 9 + 1))

test_args = (
    (range_9_0, predefined_ops, 200),
    (range_1_9, predefined_ops, 100),
    ((), predefined_ops, 200)
)

expected = ({
        "9-8+7-6-5-4-3+210",
        "9-8-7-6-5+4+3+210",
        "98+76-5+43-2-10",
        "98-7+65+43+2-1+0",
        "98-7+65+43+2-1-0"
    },
    {
        "1+2+3-4+5+6+78+9",
        "1+2+34-5+67-8+9",
        "1+23-4+5+6+78-9",
        "1+23-4+56+7+8+9",
        "12+3+4+5-6-7+89",
        "12+3-4+5+67+8+9",
        "12-3-4+5-6+7+89",
        "123+4-5+67-89",
        "123+45-67+8-9",
        "123-4-5-6-7+8-9",
        "123-45-67+89"
    },
    set()
)


def prepend(value, iterable, front=True):
    '''
        Prepend a single value in front or back of an iterable.
        prepend(1, [2, 3, 4]) -> 1 2 3 4
        prepend(1, [2, 3, 4], False) -> 2 3 4 1
    '''

    if not front:
        return chain(iterable, [value])

    return chain([value], iterable)


def merge_data(*data):
    def merge(test_args, expected):
        return prepend(expected, test_args, False)

    merged = starmap(merge, zip(*data))
    mapped = map(tuple, merged)

    return tuple(mapped)


collected = merge_data(test_args, expected)


@pytest.mark.parametrize("nums, ops, equal, expected", collected)
class TestEvalEqual:
    def test_bruteforce(self, nums, ops, equal, expected):
        expr_gen = eval_equal(nums, ops, equal)
        result = set(expr_gen)

        assert result == expected

    def test_backtracking(self, nums, ops, equal, expected):
        expr_gen = eval_equal_backtracking(nums, ops, equal)
        result = set(expr_gen)

        assert result == expected


test_args = (
    (range_9_0, 200),
    (range_1_9, 100),
    (reversed(range_1_9), 45),
    ((), 200)
)

expected = ('', '', "9+8+7+6+5+4+3+2+1", '')

collected = merge_data(test_args, expected)


@pytest.mark.parametrize("nums, equal, expected", collected)
def test_branch_and_bound(nums, equal, expected):
    expr = eval_equal_branch_and_bound(nums, equal)

    assert expr == expected
