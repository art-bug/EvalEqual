'''
    This module contains the eval_equal function and
    its various implementations and also auxiliary functions for its operation.
'''

import itertools as it_
from collections import deque
from collections.abc import Iterable


def interleave_longest(*iterables):
    '''
        Return a new iterable yielding from each iterable in turn,
        skipping any that are exhausted.

            >>> list(interleave_longest([1, 2, 3], [4, 5], [6, 7, 8]))
            [1, 4, 6, 2, 5, 7, 3, 8]

        This function may perform better for some inputs (in particular when
        the number of iterables is large).
    '''

    marker = object()
    it = it_.chain.from_iterable(it_.zip_longest(*iterables, fillvalue=marker))
    return (item for item in it if item is not marker)


def tokens(nums: Iterable[int], ops: Iterable[str]):
    '''
        Creates a token stream by interleaving numbers (digits) and operations.
    '''

    return interleave_longest(nums, ops)


def str_expr(token_gen: Iterable, sep=''):
    '''
        Stringify the token stream with a given separator.
    '''

    return sep.join(map(str, token_gen))


def prepare_exprs(nums: Iterable[int], ops: Iterable[str]):
    '''
        Creates a stream of string expressions from numbers (digits) and
        all possible combinations of operations.
    '''

    nums_it = iter(nums)
    nums, for_nums_len = it_.tee(nums_it)

    n_nums = sum(1 for _ in for_nums_len)

    if n_nums == 0:
        return ()

    n_repeats = n_nums - 1
    op_prod = it_.product(ops, repeat=n_repeats)
    nums = tuple(nums)

    expr_tokens = (tokens(nums, opers) for opers in op_prod)

    return expr_tokens


def eval_equal(nums: Iterable[int], ops: Iterable[str], equal: int):
    '''
        Generates arithmetic expressions in which the placement of operations
        is evaluated to the desired value.
    '''

    expr_tokens = prepare_exprs(nums, ops)

    if not expr_tokens:
        return expr_tokens

    exprs = map(str_expr, expr_tokens)

    suitables = filter(lambda expr: eval(expr) == equal, exprs)

    return suitables


def eval_equal_backtracking(nums: Iterable[int], ops: Iterable[str],
                            equal: int):
    '''
        The eval_equal implementation by the backtracking method.
    '''

    P = prepare_exprs(nums, ops)

    if not P:
        return P

    P = map(str_expr, P)

    S = deque()
    S.append(next(P))

    while S:
        expr = S.popleft()

        if eval(expr) == equal:
            yield expr

        next_expr = next(P, None)

        if next_expr:
            S.append(next_expr)


def eval_equal_branch_and_bound(nums: Iterable[int], equal: int):
    '''
        The eval_equal implementation (incomplete) by
        the branch-and-bound method.
    '''

    nums = tuple(nums)

    if not nums:
        return ''

    n_nums = len(nums)

    ops = [''] * (n_nums - 1)

    Sum = list(it_.chain(nums, [0]))

    for i in reversed(range(n_nums)):
        Sum[i] += Sum[i+1]

    def inner(idx: int, acc: int):
        if idx == n_nums - 1:
            return acc == equal

        L = acc - Sum[idx + 2]

        if L < equal:
            ops[idx] = '+'
            acc += nums[idx + 1]
            ret = inner(idx + 1, acc)
            if not ret:
                return ret

        L = acc + Sum[idx + 2]

        if L > equal:
            ops[idx] = '-'
            acc -= nums[idx + 1]
            ret = inner(idx + 1, acc)
            if not ret:
                return ret

        return True

    ret = inner(0, nums[0])

    if not ret:
        return ''

    expr = interleave_longest(nums, ops)

    return str_expr(expr)
