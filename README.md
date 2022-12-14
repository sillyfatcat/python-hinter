# python-hinter
CLI tool to help generate type hinting for you


```
>>> from hinter.hinter import generate_recommendation_based_on_usage
>>> generate_recommendation_based_on_usage("""foo({"foo": "bar"}, [1, 2])""")
"foo({'foo': 'bar'}: Dict[str, str], [1, 2]: List[int])"
>>> generate_recommendation_based_on_usage("""foo(1, 2)""")
'foo(1: int, 2: int)'
```