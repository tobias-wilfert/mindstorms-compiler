# Tests to check if the json is extracted correctly from the .lms input files.

import json

from src.json_parser import extract_json


def helper(filename: str, directory: str = "."):
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
    helper("empty")


# ---------- Events ----------
def test_extract_json_when_program_starts():
    helper("when_program_starts", "Events")


# ---------- Motors ----------
# - Run Motor for duration
def test_extract_json_run_motor_for_duration_base():
    helper("run_motor_for_duration_base", "Motors")


def test_extract_json_run_motor_for_duration_counterclockwise():
    helper("run_motor_for_duration_counterclockwise", "Motors")


def test_extract_json_run_motor_for_duration_degrees():
    helper("run_motor_for_duration_degrees", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors():
    helper("run_motor_for_duration_multiple_motors", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors3():
    helper("run_motor_for_duration_multiple_motors3", "Motors")


def test_extract_json_run_motor_for_duration_all_motors():
    helper("run_motor_for_duration_all_motors", "Motors")


def test_extract_json_run_motor_for_duration_seconds():
    helper("run_motor_for_duration_seconds", "Motors")


def test_extract_json_run_motor_for_duration_value_node():
    helper("run_motor_for_duration_value_node", "Motors")


def test_extract_json_run_motor_for_duration_port_list():
    helper("run_motor_for_duration_port_list", "Motors")


def test_extract_json_run_motor_for_duration_port_variable():
    helper("run_motor_for_duration_port_variable", "Motors")


def test_extract_json_run_motor_for_duration_value_variable():
    helper("run_motor_for_duration_value_variable", "Motors")


# - Motor Go to Position
def test_extract_json_motor_go_to_position_base():
    helper("motor_go_to_position_base", "Motors")


def test_extract_json_motor_go_to_position_clockwise():
    helper("motor_go_to_position_clockwise", "Motors")


def test_extract_json_motor_go_to_position_counterclockwise():
    helper("motor_go_to_position_counterclockwise", "Motors")


def test_extract_json_motor_go_to_position_multiple_motors():
    helper("motor_go_to_position_multiple_motors", "Motors")


def test_extract_json_motor_go_to_position_value_node():
    helper("motor_go_to_position_value_node", "Motors")


def test_extract_json_motor_go_to_position_port_list():
    helper("motor_go_to_position_port_list", "Motors")


def test_extract_json_motor_go_to_position_port_variable():
    helper("motor_go_to_position_port_variable", "Motors")


def test_extract_json_motor_go_to_position_value_variable():
    helper("motor_go_to_position_value_variable", "Motors")


# - Start Motor
def test_extract_json_start_motor_base():
    helper("start_motor_base", "Motors")


def test_extract_json_start_motor_all_motors():
    helper("start_motor_all_motors", "Motors")


def test_extract_json_start_motor_multiple_motors():
    helper("start_motor_multiple_motors", "Motors")


def test_extract_json_start_motor_counterclockwise():
    helper("start_motor_counterclockwise", "Motors")


def test_extract_json_start_motor_port_list():
    helper("start_motor_port_list", "Motors")


def test_extract_json_start_motor_port_variable():
    helper("start_motor_port_variable", "Motors")


# - Stop Motor
def test_extract_json_stop_motor_base():
    helper("stop_motor_base", "Motors")


def test_extract_json_stop_motor_all_motors():
    helper("stop_motor_all_motors", "Motors")


def test_extract_json_stop_motor_multiple_motors():
    helper("stop_motor_multiple_motors", "Motors")


def test_extract_json_stop_motor_port_list():
    helper("stop_motor_port_list", "Motors")


def test_extract_json_stop_motor_port_variable():
    helper("stop_motor_port_variable", "Motors")


# - Set Motor Speed
def test_extract_json_set_motor_speed_base():
    helper("set_motor_speed_base", "Motors")


def test_extract_json_set_motor_speed_all_motors():
    helper("set_motor_speed_all_motors", "Motors")


def test_extract_json_set_motor_speed_multiple_motors():
    helper("set_motor_speed_multiple_motors", "Motors")


def test_extract_json_set_motor_speed_value_node():
    helper("set_motor_speed_value_node", "Motors")


def test_extract_json_set_motor_speed_port_list():
    helper("set_motor_speed_port_list", "Motors")


def test_extract_json_set_motor_speed_port_variable():
    helper("set_motor_speed_port_variable", "Motors")


def test_extract_json_set_motor_speed_value_variable():
    helper("set_motor_speed_value_variable", "Motors")


# Motor Position
def test_extract_json_motor_position_base():
    helper("motor_position_base", "Motors")


def test_extract_json_motor_position_list():
    helper("motor_position_list", "Motors")


def test_extract_json_motor_position_variable():
    helper("motor_position_variable", "Motors")


# - Motor Speed
def test_extract_json_motor_speed_base():
    helper("motor_speed_base", "Motors")


def test_extract_json_motor_speed_list():
    helper("motor_speed_list", "Motors")


def test_extract_json_motor_speed_variable():
    helper("motor_speed_variable", "Motors")


# ---------- Operators ----------
def test_extract_json_arithmetic():
    helper("arithmetic", "Operators")


def test_extract_json_divide():
    helper("divide", "Operators")


def test_extract_json_minus():
    helper("minus", "Operators")


def test_extract_json_multiply():
    helper("multiply", "Operators")


def test_extract_json_plus():
    helper("plus", "Operators")


def test_extract_json_arithmetic_variable():
    helper("arithmetic_variable", "Operators")


# ---------- Variables ----------
def test_extract_json_change_variable_by():
    helper("change_variable_by", "Variables")


def test_extract_json_variable_num():
    helper("variable_num", "Variables")


def test_extract_json_variable_string():
    helper("variable_string", "Variables")


def test_extract_json_list():
    helper("list", "Variables")


def test_extract_json_add_item_to_list_base():
    helper("add_item_to_list_base", "Variables")


def test_extract_json_add_item_to_list_int():
    helper("add_item_to_list_int", "Variables")


def test_extract_json_add_item_to_list_list():
    helper("add_item_to_list_list", "Variables")


def test_extract_json_add_item_to_list_variable():
    helper("add_item_to_list_variable", "Variables")
