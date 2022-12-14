import ast
import re
from typing import List, Dict, Tuple


def parse_function_parameters(function_use: str) -> List:
    pattern = re.compile(r'(?<=\().*(?=\))')
    extracted_value = re.findall(pattern, function_use)[0]
    if extracted_value == '':
        return []
    elif extracted_value.startswith("(") and extracted_value.endswith(")"):
        extracted_literal = ast.literal_eval(extracted_value)
        return [extracted_literal]
    else:
        extracted_value = f"[{extracted_value}]"
    extracted_literal = ast.literal_eval(extracted_value)
    return extracted_literal


def get_candidate_based_on_type(function_parameter: str) -> str:
    value_type = type(function_parameter)
    additional_params = []
    if value_type in [list, tuple]:
        value_type = List if value_type == list else Tuple
        additional_params = list({get_candidate_based_on_type(
            value) for value in function_parameter})
        additional_params.sort()
    elif value_type == dict:
        value_type = Dict
        additional_params = list({get_candidate_based_on_type(
            value) for value in function_parameter})
        additional_params.extend({get_candidate_based_on_type(
            value) for value in function_parameter.values()})

    if str(value_type).startswith("typing."):
        return (str(value_type).split('typing.')[-1]
                + str(additional_params).replace("'", ""))
    return_value = str(value_type).split("'")[1::2][0]
    return return_value


def replace_old_function_calls_with_new(
    old_function_call: str, new_param_string: str
) -> str:
    pattern = re.compile(r'(?<=\().*(?=\))')
    return re.sub(pattern, new_param_string, old_function_call)


def generate_recommendation_based_on_usage(function_call: str) -> str:
    parameters = parse_function_parameters(function_call)
    if not parameters:
        return function_call
    print(f'{type(parameters)}')
    new_param_string = ", ".join(
        [f'"{parameter}": {get_candidate_based_on_type(parameter)}' if
         get_candidate_based_on_type(parameter) == "str" else
            f'{parameter}: {get_candidate_based_on_type(parameter)}'
         for parameter in parameters])
    return replace_old_function_calls_with_new(function_call, new_param_string)


def generate_recommendation_based_on_usages(function_calls: List[str]) -> List[str]:
    for function_call in function_calls:
        pass
