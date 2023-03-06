# Tests to check if the json is extracted correctly from the .lms input files.

import json

from src.json_parser import extract_json


def extract_helper(filename: str, directory: str = "."):
    """Helper function that contains the logic to test if the json of a certain file is extracted correctly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    :param directory: The folder that the file is in.
    :type directory: str
    """
    with open(f"tests/inputs/{directory}/{filename}/project.json", "r") as file:
        assert extract_json(
            f"tests/inputs/{directory}/{filename}/{filename}.lms"
        ) == json.load(file)


# ---------- Base ----------
def test_extract_json_empty():
    extract_helper("empty")


# ---------- Events ----------
def test_extract_json_when_program_starts():
    extract_helper("when_program_starts", "Events")


# ---------- Motors ----------
def test_extract_json_run_motor_for_duration_base():
    extract_helper("run_motor_for_duration_base", "Motors")


def test_extract_json_run_motor_for_duration_counterclockwise():
    extract_helper("run_motor_for_duration_counterclockwise", "Motors")


def test_extract_json_run_motor_for_duration_degrees():
    extract_helper("run_motor_for_duration_degrees", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors():
    extract_helper("run_motor_for_duration_multiple_motors", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors3():
    extract_helper("run_motor_for_duration_multiple_motors3", "Motors")


def test_extract_json_run_motor_for_duration_all_motors():
    extract_helper("run_motor_for_duration_all_motors", "Motors")


def test_extract_json_run_motor_for_duration_seconds():
    extract_helper("run_motor_for_duration_seconds", "Motors")


def test_extract_json_run_motor_for_duration_value_node():
    extract_helper("run_motor_for_duration_value_node", "Motors")


# ---------- Operators ----------
def test_extract_json_arithmatic():
    extract_helper("arithmatic", "Operators")


def test_extract_json_divide():
    extract_helper("divide", "Operators")


def test_extract_json_minus():
    extract_helper("minus", "Operators")


def test_extract_json_multiply():
    extract_helper("multiply", "Operators")


def test_extract_json_plus():
    extract_helper("plus", "Operators")
