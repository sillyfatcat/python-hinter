import pytest
from typing import List, Dict

from hinter.hinter import parse_function_parameters, get_candidate_based_on_type


@pytest.mark.parametrize(
    "function_call,expected",
    [
        ("""foo()""", ()),
        ("""foo(1, 2)""", (1, 2,)),
        ("""foo("bar", 1)""", ("bar", 1)),
        ("""foo("bar")""", ("bar", )),
        ("""foo((1, 2), 'bar')""", ((1, 2), "bar")),
        ("""foo((1, 2))""", ((1, 2)))
    ]
)
def test_parse_function_use(function_call, expected):
    assert parse_function_parameters(function_call) == expected


@pytest.mark.parametrize(
    "parameter,expected",
    [
        ('a', 'str'),
        (1, 'int'),
        ("a", 'str'),
        ([], 'List[]'),
        ([1], 'List[int]'),
        ({}, 'Dict[]'),
        ([1, 2], 'List[int]'),
        ([1, 'a'], 'List[int, str]')
    ]
)
def test_get_candidate_based_on_type(parameter, expected):
    assert get_candidate_based_on_type(parameter) == expected
