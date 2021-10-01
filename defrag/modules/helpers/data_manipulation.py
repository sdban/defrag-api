# Defrag - centralized API for the openSUSE Infrastructure
# Copyright (C) 2021 openSUSE contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from functools import reduce
from itertools import islice
from typing import Any, Callable, Iterable, List, Optional, Tuple

"""
Some utilities for doing data manipulation.
"""


def compose(*funcs: Tuple[Callable]) -> Callable:
    """ Compose multiple functions (right-associative) """
    def step(acc, f):
        return f(acc)

    def inner(seed):
        return reduce(step, funcs, seed)
    return inner


def base_step(acc, val):
    acc.append(val)
    return acc


def make_xform(*reducers: Tuple[Callable]) -> Callable:
    return reduce(compose, reducers)


def make_transducer(xform: Callable, step: Callable, folder: List[Any] = []) -> Callable:
    """ 'Transduce' over a transformer and a step function into a given folder
    The composition of functions as 'xform' applies right to left (right-associative). See test below. """
    def transducer(seq):
        return reduce(xform(step), seq, folder)
    return transducer


def partition_left_right(xs: Iterable, predicate: Callable) -> Tuple[List[Any], List[Any]]:
    def reducer(acc, val):
        left, right = acc
        if predicate(val):
            right.append(val)
        else:
            left.append(val)
        return acc
    return reduce(reducer, xs, ([], []))


def find_first_nogen(it: Iterable, relation: Callable[[Any, Any], bool], origin: Any) -> int:
    if not it:
        return 0
    for i, e in enumerate(it):
        if relation(e, origin):
            return i
    return -1


def find_first(it: Iterable, relation: Callable[[Any, Any], bool], origin: Any) -> int:
    if not it:
        return 0

    def gen():
        for i, e in enumerate(it):
            if relation(e, origin):
                yield i
                return
    for res in gen():
        return res
    return -1


def filter_sort_count(
    it: Iterable[Any],
    filter_pred: Optional[Callable[[Any], bool]] = None,
    count: Optional[int] = None,
    sort_pred: Optional[Callable[[Any], bool]] = None,
    reverse: bool = False
) -> List[Any]:
    filtered = (x for x in it if filter_pred(x)) if filter_pred else (x for x in it)
    counted = (x for x in islice(filtered, count)) if count else filtered
    return sorted(counted, key=lambda item: sort_pred(item), reverse=reverse) if sort_pred else sorted(counted, reverse=reverse)
