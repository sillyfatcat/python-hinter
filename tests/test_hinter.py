import pytest

from hinter.hinter import (
    generate_recommendation_based_on_usage,
    get_candidate_based_on_type,
    parse_function_parameters,
    replace_old_function_calls_with_new
)


@pytest.mark.parametrize(
    "function_call,expected",
    [
        ("""foo()""", []),
        ("""foo(1, 2)""", [1, 2, ]),
        ("""foo("bar", 1)""", ["bar", 1]),
        ("""foo("bar")""", ["bar", ]),
        ("""foo((1, 2), 'bar')""", [(1, 2), "bar"]),
        ("""foo((1, 2))""", [(1, 2)])
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


@pytest.mark.parametrize(
    "function_call,new_param_string,expected",
    [
        ("""foo()""", "", """foo()"""),
        ("""foo(1, 2)""", "1: int, 2: int", """foo(1: int, 2: int)"""),
    ]
)
def test_replace_old_function_calls_with_new(
    function_call, new_param_string, expected
):
    assert replace_old_function_calls_with_new(
        function_call, new_param_string) == expected


@pytest.mark.parametrize(
    "function_call,expected",
    [
        ("""foo()""", """foo()"""),
        ("""foo(1, 2)""", """foo(1: int, 2: int)"""),
        ("""foo("bar", 1)""", """foo("bar": str, 1: int)"""),
        ("""foo("bar")""", """foo("bar": str)"""),
        ("""foo((1, 2), 'bar')""", """foo((1, 2): Tuple[int], "bar": str)"""),
        ("""foo((1, 2))""", """foo((1, 2): Tuple[int])"""),
        ("""foo([1, 2])""", """foo([1, 2]: List[int])"""),
        ("""foo({"foo": "bar"})""", """foo({'foo': 'bar'}: Dict[str, str])"""),
        ("""foo({"foo": "bar"}, [1, 2])""",
         """foo({'foo': 'bar'}: Dict[str, str], [1, 2]: List[int])""")
    ]
)
def test_generate_recommendation_based_on_usage(function_call, expected):
    assert generate_recommendation_based_on_usage(function_call) == expected
