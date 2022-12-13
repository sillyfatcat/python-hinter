import ast
import re
from typing import List, Dict


def parse_function_parameters(function_use: str):
    pattern = re.compile(r'(?<=\().*(?=\))')
    extracted_value = re.findall(pattern, function_use)[0]
    if extracted_value == '':
        return ()
    extracted_literal = ast.literal_eval(extracted_value)
    if not isinstance(extracted_literal, tuple):
        extracted_literal = tuple([extracted_literal])
    return extracted_literal


def get_candidate_based_on_type(function_parameter: str):
    value_type = type(function_parameter)
    additional_params = []
    if value_type == list:
        value_type = List
        additional_params = list({get_candidate_based_on_type(
            value) for value in function_parameter})
    elif value_type == dict:
        value_type = Dict
    if str(value_type).startswith("typing."):
        return (str(value_type).split('typing.')[-1]
                + str(additional_params).replace("'", ""))
    return_value = str(value_type).split("'")[1::2][0]
    return return_value


def generate_recommendation_based_on_usage(function_calls: List[str]):
    pass
