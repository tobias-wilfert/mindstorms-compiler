# Tests to check if the json is extracted correctly from the .lms input files.

import json

from src.json_parser import extract_json


def extract_helper(filename: str):
    """Helper function that contains the logic to test if the json of a certain file is extracted correctly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    """
    with open(f"tests/inputs/{filename}/project.json", "r") as file:
        assert extract_json(f"tests/inputs/{filename}/{filename}.lms") == json.load(
            file
        )


def test_extract_json_empty():
    extract_helper("empty")


def test_extract_json_run_motor_for_duration_base():
    extract_helper("run_motor_for_duration_base")


def test_extract_json_run_motor_for_duration_counterclockwise():
    extract_helper("run_motor_for_duration_counterclockwise")


def test_extract_json_run_motor_for_duration_degrees():
    extract_helper("run_motor_for_duration_degrees")


def test_extract_json_run_motor_for_duration_multiple_motors():
    extract_helper("run_motor_for_duration_multiple_motors")


def test_extract_json_run_motor_for_duration_multiple_motors3():
    extract_helper("run_motor_for_duration_multiple_motors3")


def test_extract_json_run_motor_for_duration_all_motors():
    extract_helper("run_motor_for_duration_all_motors")


def test_extract_json_run_motor_for_duration_seconds():
    extract_helper("run_motor_for_duration_seconds")


def test_extract_json_when_program_starts():
    extract_helper("when_program_starts")


def test_extract_json_run_motor_for_duration_value_node():
    extract_helper("run_motor_for_duration_value_node")


def test_extract_json_arithmatic():
    extract_helper("arithmatic")


def test_extract_json_divide():
    extract_helper("divide")


def test_extract_json_minus():
    extract_helper("minus")


def test_extract_json_multiply():
    extract_helper("multiply")


def test_extract_json_plus():
    extract_helper("plus")
