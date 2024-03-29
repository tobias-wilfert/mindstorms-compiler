# Test to check that the Code is generated correctly
from pytest import raises

from src.code_generator import CodeGenerator
from src.json_parser import extract_json, filter_json
from src.visitor import Visitor

includes = """from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
"""


def helper(filename: str, directory: str = ".") -> str:
    """Helper function that contains thee logic to test if the ast for a certain file is generated correctly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    :return: String representation of the AST.
    :rtype: str
    """
    concrete_syntax_tree = filter_json(
        extract_json(f"tests/inputs/{directory}/{filename}/{filename}.lms")
    )
    visitor = Visitor(best_effort=True)
    abstract_syntax_tree = visitor.visit(concrete_syntax_tree)
    code_generator = CodeGenerator()
    return code_generator.generate(abstract_syntax_tree)


# ---------- Base ----------
# Verified on Hardware.
def test_code_empty():
    assert (
        helper("empty")
        == f"""{includes}
# Create your objects here.

# Write your program here.

"""
    )


# ---------- Events ----------
# Verified on Hardware.
def test_code_when_program_starts():
    assert (
        helper("when_program_starts", "Events")
        == f"""{includes}
# Create your objects here.

# Write your program here.

"""
    )


# ---------- Motors ----------
# - Run Motor for duration
# Verified on Hardware.
def test_code_run_motor_for_duration_base():
    assert (
        helper("run_motor_for_duration_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations(1.0)

"""
    )


# Verified on Hardware.
def test_code_run_motor_for_duration_counterclockwise():
    assert (
        helper("run_motor_for_duration_counterclockwise", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations(-1.0)

"""
    )


# Verified on Hardware.
def test_code_run_motor_for_duration_degrees():
    assert (
        helper("run_motor_for_duration_degrees", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_degrees(int(1.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_run_motor_for_duration_multiple_motors():
    assert (
        helper("run_motor_for_duration_multiple_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_e = Motor('E')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.run_for_rotations(1.0)
motor_e.run_for_rotations(1.0)

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_run_motor_for_duration_multiple_motors3():
    assert (
        helper("run_motor_for_duration_multiple_motors3", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')
motor_c = Motor('C')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.run_for_rotations(1.0)
motor_b.run_for_rotations(1.0)
motor_c.run_for_rotations(1.0)

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_run_motor_for_duration_all_motors():
    assert (
        helper("run_motor_for_duration_all_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')
motor_c = Motor('C')
motor_d = Motor('D')
motor_e = Motor('E')
motor_f = Motor('F')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.run_for_rotations(1.0)
motor_b.run_for_rotations(1.0)
motor_c.run_for_rotations(1.0)
motor_d.run_for_rotations(1.0)
motor_e.run_for_rotations(1.0)
motor_f.run_for_rotations(1.0)

"""
    )


# Verified on Hardware
def test_code_run_motor_for_duration_seconds():
    assert (
        helper("run_motor_for_duration_seconds", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_seconds(1.0)

"""
    )


# Verified on Hardware
def test_code_run_motor_for_duration_value_node():
    assert (
        helper("run_motor_for_duration_value_node", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 + 2.0))

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_run_motor_for_duration_port_list():
    assert (
        helper("run_motor_for_duration_port_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).run_for_rotations(1.0)

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_run_motor_for_duration_port_variable():
    assert (
        helper("run_motor_for_duration_port_variable", "Motors")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).run_for_rotations(1.0)

"""
    )


# Verified on Hardware
def test_code_run_motor_for_duration_value_variable():
    assert (
        helper("run_motor_for_duration_value_variable", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 0.0
motor_a.run_for_rotations(my_variable)

"""
    )


# - Motor Go to Position
# Verified on Hardware
def test_code_motor_go_to_position_base():
    assert (
        helper("motor_go_to_position_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_to_position(int(0.0), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_motor_go_to_position_clockwise():
    assert (
        helper("motor_go_to_position_clockwise", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_to_position(int(0.0), 'clockwise')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_motor_go_to_position_counterclockwise():
    assert (
        helper("motor_go_to_position_counterclockwise", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_to_position(int(0.0), 'counterclockwise')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_motor_go_to_position_multiple_motors():
    assert (
        helper("motor_go_to_position_multiple_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.run_to_position(int(0.0), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.
motor_b.run_to_position(int(0.0), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_motor_go_to_position_value_node():
    assert (
        helper("motor_go_to_position_value_node", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_to_position(int((1.0 + 2.0)), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_motor_go_to_position_port_list():
    assert (
        helper("motor_go_to_position_port_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).run_to_position(int(0.0), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_motor_go_to_position_port_variable():
    assert (
        helper("motor_go_to_position_port_variable", "Motors")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).run_to_position(int(0.0), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_motor_go_to_position_value_variable():
    assert (
        helper("motor_go_to_position_value_variable", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 0.0
motor_a.run_to_position(int(my_variable), 'shortest path')  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# - Start Motor
# Verified on Hardware
def test_code_start_motor_base():
    assert (
        helper("start_motor_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.start()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_start_motor_all_motors():
    assert (
        helper("start_motor_all_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')
motor_c = Motor('C')
motor_d = Motor('D')
motor_e = Motor('E')
motor_f = Motor('F')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.start()
motor_b.start()
motor_c.start()
motor_d.start()
motor_e.start()
motor_f.start()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_start_motor_multiple_motors():
    assert (
        helper("start_motor_multiple_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.start()
motor_b.start()

"""
    )


# Verified on Hardware
def test_code_start_motor_counterclockwise():
    assert (
        helper("start_motor_counterclockwise", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.start(-motor_a.get_default_speed())

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_start_motor_port_list():
    assert (
        helper("start_motor_port_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).start()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_start_motor_port_variable():
    assert (
        helper("start_motor_port_variable", "Motors")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).start()

"""
    )


# - Stop Motor
# Verified on Hardware
def test_code_stop_motor_base():
    assert (
        helper("stop_motor_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.stop()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_stop_motor_all_motors():
    assert (
        helper("stop_motor_all_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')
motor_c = Motor('C')
motor_d = Motor('D')
motor_e = Motor('E')
motor_f = Motor('F')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.stop()
motor_b.stop()
motor_c.stop()
motor_d.stop()
motor_e.stop()
motor_f.stop()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_stop_motor_multiple_motors():
    assert (
        helper("stop_motor_multiple_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.stop()
motor_b.stop()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_stop_motor_port_list():
    assert (
        helper("stop_motor_port_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).stop()

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_stop_motor_port_variable():
    assert (
        helper("stop_motor_port_variable", "Motors")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).stop()

"""
    )


# - Set Motor Speed
# Verified on Hardware
def test_code_set_motor_speed_base():
    assert (
        helper("set_motor_speed_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_set_motor_speed_all_motors():
    assert (
        helper("set_motor_speed_all_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')
motor_c = Motor('C')
motor_d = Motor('D')
motor_e = Motor('E')
motor_f = Motor('F')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_b.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_c.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_d.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_e.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_f.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_set_motor_speed_multiple_motors():
    assert (
        helper("set_motor_speed_multiple_motors", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')
motor_b = Motor('B')

# Write your program here.
# Note: This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
motor_a.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.
motor_b.set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_set_motor_speed_value_node():
    assert (
        helper("set_motor_speed_value_node", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.set_default_speed(int((25.0 + 50.0)))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_set_motor_speed_list():
    assert (
        helper("set_motor_speed_port_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_set_motor_speed_port_variable():
    assert (
        helper("set_motor_speed_port_variable", "Motors")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).set_default_speed(int(75.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_set_motor_speed_value_variable():
    assert (
        helper("set_motor_speed_value_variable", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 75.0
motor_a.set_default_speed(int(my_variable))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# - Motor Position
# Verified on Hardware
def test_code_motor_position_base():
    assert (
        helper("motor_position_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations(motor_a.get_position())

"""
    )


# Verified on Hardware
def test_code_motor_position_list():
    assert (
        helper("motor_position_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []
motor_a = Motor('A')

# Write your program here.
my_list.append('A')
motor_a.run_for_rotations(Motor(my_list[0]).get_position())

"""
    )


# Verified on Hardware
def test_code_motor_position_variable():
    assert (
        helper("motor_position_variable", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 'A'
motor_a.run_for_rotations(Motor(my_variable[0]).get_position())

"""
    )


# - Motor Speed
# Verified on Hardware
def test_code_motor_speed_base():
    assert (
        helper("motor_speed_base", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations(motor_a.get_speed())

"""
    )


# Verified on Hardware
def test_code_motor_speed_list():
    assert (
        helper("motor_speed_list", "Motors")
        == f"""{includes}
# Create your objects here.
my_list = []
motor_a = Motor('A')

# Write your program here.
my_list.append('A')
motor_a.run_for_rotations(Motor(my_list[0]).get_speed())

"""
    )


# Verified on Hardware
def test_code_motor_speed_variable():
    assert (
        helper("motor_speed_variable", "Motors")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 'A'
motor_a.run_for_rotations(Motor(my_variable[0]).get_speed())

"""
    )


# # ---------- Movement ----------
# - Move for duration
# Verified on Hardware
def test_code_move_for_duration_backwards():
    assert (
        helper("move_for_duration_backwards", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(-10.0, 'cm')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_base():
    assert (
        helper("move_for_duration_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'cm')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_clockwise():
    assert (
        helper("move_for_duration_clockwise", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'cm', 100)

"""
    )


# Verified on Hardware
def test_code_move_for_duration_counterclockwise():
    assert (
        helper("move_for_duration_counterclockwise", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'cm', -100)

"""
    )


# Verified on Hardware
def test_code_move_for_duration_degrees():
    assert (
        helper("move_for_duration_degrees", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'degrees')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_inches():
    assert (
        helper("move_for_duration_inches", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'in')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_rotations():
    assert (
        helper("move_for_duration_rotations", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'rotations')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_seconds():
    assert (
        helper("move_for_duration_seconds", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'seconds')

"""
    )


# Verified on Hardware
def test_code_move_for_duration_value_variable():
    assert (
        helper("move_for_duration_value_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 10.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(my_variable, 'cm')

"""
    )


# - Move with Steering
# Verified on Hardware
def test_code_move_with_steering_base():
    assert (
        helper("move_with_steering_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'cm', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_degrees():
    assert (
        helper("move_with_steering_degrees", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'degrees', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_inches():
    assert (
        helper("move_with_steering_inches", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'in', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_rotations():
    assert (
        helper("move_with_steering_rotations", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'rotations', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_seconds():
    assert (
        helper("move_with_steering_seconds", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'seconds', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_steering_variable():
    assert (
        helper("move_with_steering_steering_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 0.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(10.0, 'cm', int(my_variable))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_move_with_steering_value_variable():
    assert (
        helper("move_with_steering_value_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 10.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.move(my_variable, 'cm', int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# - Start Moving with Steering
# Verified on Hardware
def test_code_start_moving_with_steering_base():
    assert (
        helper("start_moving_with_steering_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.start(int(0.0))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# Verified on Hardware
def test_code_start_moving_with_steering_variable():
    assert (
        helper("start_moving_with_steering_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 0.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.start(int(my_variable))  # Note: This method expects an integer so wee need to convert the value.

"""
    )


# - Stop Moving
# Verified on Hardware
def test_code_stop_moving():
    assert (
        helper("stop_moving", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.start(int(0.0))  # Note: This method expects an integer so wee need to convert the value.
motor_pair.stop()

"""
    )


# - Set Movement Speed
# Verified on Hardware
def test_code_set_movement_speed_base():
    assert (
        helper("set_movement_speed_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_default_speed(int(50.0))  # Note: This method expects an integer so wee need to convert the value.
motor_pair.move(10.0, 'cm')

"""
    )


# Verified on Hardware
def test_code_set_movement_speed_value_variable():
    assert (
        helper("set_movement_speed_value_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 10.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_default_speed(int(my_variable))  # Note: This method expects an integer so wee need to convert the value.
motor_pair.move(10.0, 'cm')

"""
    )


# - Set Movement Motors
# Verified on Hardware
def test_code_set_movement_motors_base():
    assert (
        helper("set_movement_motors_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.

"""
    )


# Verified on Hardware
def test_code_set_movement_motors_list():
    assert (
        helper("set_movement_motors_list", "Movement")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
my_list.append('B')
# Note: This will fail if the first two items in my_list are not valid ports.
motor_pair = MotorPair(my_list[0], my_list[1])
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.

"""
    )


# Verified on Hardware
def test_code_set_movement_motors_variable():
    assert (
        helper("set_movement_motors_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'AB'
# Note: This will fail if the first two items in my_variable are not valid ports.
motor_pair = MotorPair(my_variable[0], my_variable[1])
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.

"""
    )


# - Set Motor rotation
# Verified on Hardware
def test_code_set_motor_rotation_base():
    assert (
        helper("set_motor_rotation_base", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_motor_rotation(17.5, 'cm')
motor_pair.move(10.0, 'cm')

"""
    )


# Verified on Hardware
def test_code_set_motor_rotation_inches():
    assert (
        helper("set_motor_rotation_inches", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_motor_rotation(17.5, 'in')
motor_pair.move(10.0, 'cm')

"""
    )


# Verified on Hardware
def test_code_set_motor_rotation_value_variable():
    assert (
        helper("set_motor_rotation_value_variable", "Movement")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 10.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_motor_rotation(my_variable, 'cm')
motor_pair.move(10.0, 'cm')

"""
    )


# ---------- Light ----------
# - Start Animation
# No Verification Needed
def test_code_start_animation_base():
    assert (
        helper("start_animation_base", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_start_animation_custom():
    assert (
        helper("start_animation_custom", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.

"""
    )


# - Play Animation until done
# No Verification Needed
def test_code_play_animation_until_done_base():
    assert (
        helper("play_animation_until_done_base", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_play_animation_until_done_custom():
    assert (
        helper("play_animation_until_done_custom", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.

"""
    )


# - Turn on for duration
# Verified on Hardware
def test_code_turn_on_for_duration_base():
    assert (
        helper("turn_on_for_duration_base", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
_turn_on_pattern('9909999099000009000909990')
wait_for_seconds(int(2.0))
hub.light_matrix.off()

"""
    )


# Verified on Hardware
def test_code_turn_on_for_duration_custom():
    assert (
        helper("turn_on_for_duration_custom", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
_turn_on_pattern('0000009990099900999000000')
wait_for_seconds(int(2.0))
hub.light_matrix.off()

"""
    )


# Verified on Hardware
def test_code_turn_on_for_duration_variable():
    assert (
        helper("turn_on_for_duration_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
my_variable = 3.0
_turn_on_pattern('9909999099000009000909990')
wait_for_seconds(int(my_variable))
hub.light_matrix.off()

"""
    )


# - Turn on
# Verified on Hardware
def test_code_turn_on_base():
    assert (
        helper("turn_on_base", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
_turn_on_pattern('9909999099000009000909990')

"""
    )


# Verified on Hardware
def test_code_turn_on_custom():
    assert (
        helper("turn_on_custom", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
_turn_on_pattern('0000009990099900999000000')

"""
    )


# - Write
# Verified on Hardware
def test_code_write_base():
    assert (
        helper("write_base", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write('Hello World')

"""
    )


# Verified on Hardware
def test_code_write_variable():
    assert (
        helper("write_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 'Hello World'
hub.light_matrix.write(my_variable)

"""
    )


# - Turn off
# Verified on Hardware
def test_code_turn_off_pixels():
    assert (
        helper("turn_off_pixels", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.off()

"""
    )


# - Set pixel brightness
# Verified on Hardware
def test_code_set_pixel_brightness_base():
    assert (
        helper("set_pixel_brightness_base", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
_brightness = 75.0
_turn_on_pattern('9909999099000009000909990', _brightness)

"""
    )


# Verified on Hardware
def test_code_set_pixel_brightness_variable():
    assert (
        helper("set_pixel_brightness_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Declare you functions here.
# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))

# Write your program here.
my_variable = 50.0
_brightness = my_variable
_turn_on_pattern('9909999099000009000909990', _brightness)

"""
    )


# - Set pixel
# Verified on Hardware
def test_code_set_pixel_base():
    assert (
        helper("set_pixel_base", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.set_pixel(int(1.0)-1, int(1.0)-1, int(100.0))  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.

"""
    )


# Verified on Hardware
def test_code_set_pixel_variable():
    assert (
        helper("set_pixel_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 50.0
hub.light_matrix.set_pixel(int(1.0)-1, int(1.0)-1, int(my_variable))  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.

"""
    )


# Verified on Hardware
def test_code_set_pixel_x_value_variable():
    assert (
        helper("set_pixel_x_value_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 2.0
hub.light_matrix.set_pixel(int(my_variable)-1, int(1.0)-1, int(100.0))  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.

"""
    )


# Verified on Hardware
def test_code_set_pixel_y_value_variable():
    assert (
        helper("set_pixel_y_value_variable", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 2.0
hub.light_matrix.set_pixel(int(1.0)-1, int(my_variable)-1, int(100.0))  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.

"""
    )


# - Rotate Orientation
# No Verification Needed
def test_code_rotate_orientation_clockwise():
    assert (
        helper("rotate_orientation_clockwise", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_rotate_orientation_counterclockwise():
    assert (
        helper("rotate_orientation_counterclockwise", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# - Set Orientation
# No Verification Needed
def test_code_set_orientation_upright():
    assert (
        helper("set_orientation_upright", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_set_orientation_upsidedown():
    assert (
        helper("set_orientation_upsidedown", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_set_orientation_left():
    assert (
        helper("set_orientation_left", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# No Verification Needed
def test_code_set_orientation_right():
    assert (
        helper("set_orientation_right", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.

"""
    )


# - Set Center button
# Verified on Hardware
def test_code_set_center_button_red():
    assert (
        helper("set_center_button_red", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('red')

"""
    )


# Verified on Hardware
def test_code_set_center_button_yellow():
    assert (
        helper("set_center_button_yellow", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('yellow')

"""
    )


# Verified on Hardware
def test_code_set_center_button_green():
    assert (
        helper("set_center_button_green", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('green')

"""
    )


# Verified on Hardware
def test_code_set_center_button_cyan():
    assert (
        helper("set_center_button_cyan", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('cyan')

"""
    )


# Verified on Hardware
def test_code_set_center_button_azure():
    assert (
        helper("set_center_button_azure", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('azure')

"""
    )


# Verified on Hardware
def test_code_set_center_button_pink():
    assert (
        helper("set_center_button_pink", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('pink')

"""
    )


# Verified on Hardware
def test_code_set_center_button_white():
    assert (
        helper("set_center_button_white", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('white')

"""
    )


# Verified on Hardware
def test_code_set_center_button_black():
    assert (
        helper("set_center_button_black", "Light")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.status_light.on('black')

"""
    )


# -Light up distance sensor
# Verified on Hardware
def test_code_light_up_distance_sensor_base():
    assert (
        helper("light_up_distance_sensor_base", "Light")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')

# Write your program here.
distance_sensor_a.light_up(100, 100, 100, 100)

"""
    )


# Verified on Hardware
def test_code_light_up_distance_sensor_port_list():
    assert (
        helper("light_up_distance_sensor_port_list", "Light")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
# Note: This will fail if the first item in my_list is not valid port.
DistanceSensor(my_list[0].upper()).light_up(100, 100, 100, 100)

"""
    )


# Verified on Hardware
def test_code_light_up_distance_sensor_port_variable():
    assert (
        helper("light_up_distance_sensor_port_variable", "Light")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: This will fail if the first item in my_variable is not valid port.
DistanceSensor(my_variable[0].upper()).light_up(100, 100, 100, 100)

"""
    )


# ---------- Sound ----------
# - Play sound until done base
# Verified on Hardware
def test_code_play_sound_until_done_base():
    assert (
        helper("play_sound_until_done_base", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.play_sound('Cat Meow 1')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_play_sound_until_done_custom():
    assert (
        helper("play_sound_until_done_custom", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.play_sound('Cat Meow 1')
hub.light_matrix.write('Y')

"""
    )


# - Start sound
# Verified on Hardware
def test_code_start_sound_base():
    assert (
        helper("start_sound_base", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.start_sound('Cat Meow 1')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_start_sound_custom():
    assert (
        helper("start_sound_custom", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.start_sound('Cat Meow 1')
hub.light_matrix.write('Y')

"""
    )


# - Play beep
# Verified on Hardware
def test_code_play_beep_base():
    assert (
        helper("play_beep_base", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.speaker.beep(60.0, 0.2)

"""
    )


# Verified on Hardware
def test_code_play_beep_variable():
    assert (
        helper("play_beep_variable", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
pitch = 60.0
duration = 0.5
hub.speaker.beep(pitch, duration)

"""
    )


# - Start beep
# Verified on Hardware
def test_code_start_beep_base():
    assert (
        helper("start_beep_base", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.speaker.start_beep(60.0)

"""
    )


# Verified on Hardware
def test_code_start_beep_variable():
    assert (
        helper("start_beep_variable", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 60.0
hub.speaker.start_beep(my_variable)

"""
    )


# - Stop beep
# Verified on Hardware
def test_code_stop_beep():
    assert (
        helper("stop_beep", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.speaker.start_beep(60.0)
wait_for_seconds(0.5)
hub.speaker.stop()

"""
    )


# - Change Pitch
# Verified on Hardware
def test_code_change_pitch_effect():
    assert (
        helper("change_pitch_effect", "Sound")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the CHANGE PITCH block. Note: that pitch effects are not supported in Python at the moment.

"""
    )


# - Set Pitch
# Verified on Hardware
def test_code_set_pitch_effect():
    assert (
        helper("set_pitch_effect", "Sound")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the SET PITCH block. Note: that pitch effects are not supported in Python at the moment.

"""
    )


# - Clear Sound Effects
# Verified on Hardware
def test_code_clear_sound_effects():
    assert (
        helper("clear_sound_effects", "Sound")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the CLEAR PITCH block. Note: that pitch effects are not supported in Python at the moment.

"""
    )


# - Change volume
# Verified on Hardware
def test_code_change_volume_base():
    assert (
        helper("change_volume_base", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.play_sound('Cat Meow 1')
hub.speaker.set_volume(hub.speaker.get_volume() - -10.0)
app.play_sound('Cat Meow 1')

"""
    )


# Verified on Hardware
def test_code_change_volume_variable():
    assert (
        helper("change_volume_variable", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
my_variable = 10.0
app.play_sound('Cat Meow 1')
hub.speaker.set_volume(hub.speaker.get_volume() - my_variable)
app.play_sound('Cat Meow 1')

"""
    )


# - Set volume
# Verified on Hardware
def test_code_set_volume_base():
    assert (
        helper("set_volume_base", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
app.play_sound('Cat Meow 1')
hub.speaker.set_volume(50.0)
app.play_sound('Cat Meow 1')

"""
    )


# Verified on Hardware
def test_code_set_volume_variable():
    assert (
        helper("set_volume_variable", "Sound")
        == f"""{includes}
# Create your objects here.
app = App()
hub = MSHub()

# Write your program here.
my_variable = 50.0
app.play_sound('Cat Meow 1')
hub.speaker.set_volume(my_variable)
app.play_sound('Cat Meow 1')

"""
    )


# - Volume
# Verified on Hardware
def test_code_volume():
    assert (
        helper("volume", "Sound")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(hub.speaker.get_volume())

"""
    )


# ---------- Control ----------
# - Wait for seconds
# Verified on Hardware
def test_code_wait_for_seconds_base():
    assert (
        helper("wait_for_seconds_base", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_for_seconds(1.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_wait_for_seconds_variable():
    assert (
        helper("wait_for_seconds_variable", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 2.0
wait_for_seconds(my_variable)
hub.light_matrix.write('Y')

"""
    )


# - Wait until
# Verified on Hardware
def test_code_wait_until():
    assert (
        helper("wait_until", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_gesture() == 'shaken')
hub.light_matrix.write('Y')

"""
    )


# - Repeat loop
# Verified on Hardware
def test_code_repeat_loop_base():
    assert (
        helper("repeat_loop_base", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
for _ in range(3.0):
\thub.light_matrix.write('Y')
\thub.light_matrix.write('_')

"""
    )


# Verified on Hardware
def test_code_repeat_loop_variable():
    assert (
        helper("repeat_loop_variable", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 2.0
for _ in range(my_variable):
\thub.light_matrix.write('Y')
\thub.light_matrix.write('_')

"""
    )


# - Forever loop
# Verified on Hardware
def test_code_forever_loop():
    assert (
        helper("forever_loop", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
while True:
\thub.light_matrix.write('Y')
\thub.light_matrix.write('_')

"""
    )


# - Repeat until loop
# Verified on Hardware
def test_code_repeat_until_loop():
    assert (
        helper("repeat_until_loop", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
while not (hub.motion_sensor.get_gesture() == 'shaken'):
\thub.light_matrix.write('Y')
\thub.light_matrix.write('_')

"""
    )


# - If then
# Verified on Hardware
def test_code_if_then():
    assert (
        helper("if_then", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if (1.0 == 1.0):
\thub.light_matrix.write('Y')

"""
    )


# - If then else
# Verified on Hardware
def test_code_if_then_else():
    assert (
        helper("if_then_else", "Control")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if (1.0 == 2.0):
\thub.light_matrix.write('Y')
else:
\thub.light_matrix.write('N')

"""
    )


# - Do this and this
# Verified on Hardware
def test_code_do_this_and_this():
    assert (
        helper("do_this_and_this", "Control")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the DO THIS AND THIS block. Note: that parallelism is not supported in Python at the moment.

"""
    )


# - Stop other stacks
# Verified on Hardware
def test_code_stop_other_stacks():
    assert (
        helper("stop_other_stacks", "Control")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the STOP OTHER STACKS block. Note: that parallelism is not supported in Python at the moment.

"""
    )


# - Stop
# Verified on Hardware
def test_code_stop_base():
    assert (
        helper("stop_base", "Control")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the STOP block. Note: that parallelism is not supported in Python at the moment.

"""
    )


# Verified on Hardware
def test_code_stop_this_stack():
    assert (
        helper("stop_this_stack", "Control")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the STOP block. Note: that parallelism is not supported in Python at the moment.

"""
    )


# Verified on Hardware
def test_code_stop_exit_program():
    assert (
        helper("stop_exit_program", "Control")
        == f"""{includes}
# Create your objects here.

# Write your program here.
# Placeholder for the STOP block. Note: that parallelism is not supported in Python at the moment.

"""
    )


# ---------- Sensors ----------
# - Is color
# black
# Verified on Hardware
def test_code_is_color_black():
    assert (
        helper("is_color_black", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'black')
hub.light_matrix.write('Y')

"""
    )


# violet
# Verified on Hardware
def test_code_is_color_violet():
    assert (
        helper("is_color_violet", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'violet')
hub.light_matrix.write('Y')

"""
    )


# blue
# Verified on Hardware
def test_code_is_color_blue():
    assert (
        helper("is_color_blue", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'blue')
hub.light_matrix.write('Y')

"""
    )


# light blue
# Verified on Hardware
def test_code_is_color_light_blue():
    assert (
        helper("is_color_light_blue", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'cyan')
hub.light_matrix.write('Y')

"""
    )


# green
# Verified on Hardware
def test_code_is_color_green():
    assert (
        helper("is_color_green", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'green')
hub.light_matrix.write('Y')

"""
    )


# yellow
# Verified on Hardware
def test_code_is_color_yellow():
    assert (
        helper("is_color_yellow", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'yellow')
hub.light_matrix.write('Y')

"""
    )


# red
# Verified on Hardware
def test_code_is_color_red():
    assert (
        helper("is_color_red", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'red')
hub.light_matrix.write('Y')

"""
    )


# white
# Verified on Hardware
def test_code_is_color_white():
    assert (
        helper("is_color_white", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == 'white')
hub.light_matrix.write('Y')

"""
    )


# no color
# Verified on Hardware
def test_code_is_color_no_color():
    assert (
        helper("is_color_no_color", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_color() == None)
hub.light_matrix.write('Y')

"""
    )


# - Color
# Verified on Hardware
def test_code_color():
    assert (
        helper("color", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
color_sensor_a = ColorSensor('A')

# Write your program here.
hub.light_matrix.write({{None:-1, 'black':0, 'violet':1, 'blue':3, 'cyan':4, 'green':5, 'yellow': 7, 'red':9, 'white':10}}[color_sensor_a.get_color()])

"""
    )


# - Is reflected light
# Verified on Hardware
def test_code_is_reflected_light_base():
    assert (
        helper("is_reflected_light_base", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_reflected_light() < 50.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_reflected_light_equal():
    assert (
        helper("is_reflected_light_equal", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_reflected_light() == 50.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_reflected_light_greater():
    assert (
        helper("is_reflected_light_greater", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: color_sensor_a.get_reflected_light() > 50.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_reflected_light_variable():
    assert (
        helper("is_reflected_light_variable", "Sensors")
        == f"""{includes}
# Create your objects here.
color_sensor_a = ColorSensor('A')
hub = MSHub()

# Write your program here.
my_variable = 75.0
wait_until(lambda: color_sensor_a.get_reflected_light() < my_variable)
hub.light_matrix.write('Y')

"""
    )


# - Reflected light
# Verified on Hardware
def test_code_reflected_light():
    assert (
        helper("reflected_light", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
color_sensor_a = ColorSensor('A')

# Write your program here.
hub.light_matrix.write(color_sensor_a.get_reflected_light())

"""
    )


# - Is distance
# Verified on Hardware
def test_code_is_distance_base():
    assert (
        helper("is_distance_base", "Sensors")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: distance_sensor_a.get_distance_percentage() < 15.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_distance_cm():
    assert (
        helper("is_distance_cm", "Sensors")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: distance_sensor_a.get_distance_cm() < 15.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_distance_inches():
    assert (
        helper("is_distance_inches", "Sensors")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: distance_sensor_a.get_distance_inches() < 5.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_distance_exactly_at():
    assert (
        helper("is_distance_exactly_at", "Sensors")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: distance_sensor_a.get_distance_percentage() == 15.0)
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_distance_farther_than():
    assert (
        helper("is_distance_farther_than", "Sensors")
        == f"""{includes}
# Create your objects here.
distance_sensor_a = DistanceSensor('A')
hub = MSHub()

# Write your program here.
wait_until(lambda: distance_sensor_a.get_distance_percentage() > 15.0)
hub.light_matrix.write('Y')

"""
    )


# - Distance
# Verified on Hardware
def test_code_distance_base():
    assert (
        helper("distance_base", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
distance_sensor_a = DistanceSensor('A')

# Write your program here.
hub.light_matrix.write(distance_sensor_a.get_distance_percentage())

"""
    )


# Verified on Hardware
def test_code_distance_cm():
    assert (
        helper("distance_cm", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
distance_sensor_a = DistanceSensor('A')

# Write your program here.
hub.light_matrix.write(distance_sensor_a.get_distance_cm())

"""
    )


# Verified on Hardware
def test_code_distance_inches():
    assert (
        helper("distance_inches", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
distance_sensor_a = DistanceSensor('A')

# Write your program here.
hub.light_matrix.write(distance_sensor_a.get_distance_inches())

"""
    )


# - Gesture
# Verified on Hardware
def test_code_gesture():
    assert (
        helper("gesture", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write({{None:-1, 'shaken':0, 'tapped':1, 'falling':3}}[hub.motion_sensor.get_gesture()])

"""
    )


# - Is hub shaken
# Verified on Hardware
def test_code_is_hub_shaken_base():
    assert (
        helper("is_hub_shaken_base", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_gesture() == 'shaken')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_shaken_falling():
    assert (
        helper("is_hub_shaken_falling", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_gesture() == 'falling')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_shaken_tapped():
    assert (
        helper("is_hub_shaken_tapped", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_gesture() == 'tapped')
hub.light_matrix.write('Y')

"""
    )


# - Is hub orientation
# Verified on Hardware
def test_code_is_hub_orientation_base():
    assert (
        helper("is_hub_orientation_base", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'front')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_orientation_back():
    assert (
        helper("is_hub_orientation_back", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'back')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_orientation_bottom():
    assert (
        helper("is_hub_orientation_bottom", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'down')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_orientation_left_side():
    assert (
        helper("is_hub_orientation_left_side", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'leftside')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_orientation_right_side():
    assert (
        helper("is_hub_orientation_right_side", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'rightside')
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_hub_orientation_top():
    assert (
        helper("is_hub_orientation_top", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.motion_sensor.get_orientation() == 'up')
hub.light_matrix.write('Y')

"""
    )


# - Hub orientation
# Verified on Hardware
def test_code_hub_orientation():
    assert (
        helper("hub_orientation", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write({{'front':0, 'back':1, 'up':2, 'down':3, 'leftside':4, 'rightside':5}}[hub.motion_sensor.get_orientation()])

"""
    )


# - Set yaw angle
# Verified on Hardware
def test_code_set_yaw_angle():
    assert (
        helper("set_yaw_angle", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.motion_sensor.reset_yaw_angle()
hub.light_matrix.write({{'front':0, 'back':1, 'up':2, 'down':3, 'leftside':4, 'rightside':5}}[hub.motion_sensor.get_orientation()])

"""
    )


# - Is button pressed
# Verified on Hardware
def test_code_is_button_pressed_base():
    assert (
        helper("is_button_pressed_base", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.left_button.is_pressed())
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_button_pressed_released():
    assert (
        helper("is_button_pressed_released", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.left_button.is_released())
hub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_button_pressed_right():
    assert (
        helper("is_button_pressed_right", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
wait_until(lambda: hub.right_button.is_pressed())
hub.light_matrix.write('Y')

"""
    )


# - Hub angle
# Verified on Hardware
def test_code_hub_angle_base():
    assert (
        helper("hub_angle_base", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(hub.motion_sensor.get_pitch_angle())

"""
    )


# Verified on Hardware
def test_code_hub_angle_roll():
    assert (
        helper("hub_angle_roll", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(hub.motion_sensor.get_roll_angle())

"""
    )


# Verified on Hardware
def test_code_hub_angle_yaw():
    assert (
        helper("hub_angle_yaw", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(hub.motion_sensor.get_yaw_angle())

"""
    )


# - Timer
# Verified on Hardware
def test_code_timer():
    assert (
        helper("timer", "Sensors")
        == f"""{includes}
# Create your objects here.
hub = MSHub()
timer = Timer()

# Write your program here.
hub.light_matrix.write(timer.now())

"""
    )


# - Reset timer
# Verified on Hardware
def test_code_reset_timer():
    assert (
        helper("reset_timer", "Sensors")
        == f"""{includes}
# Create your objects here.
timer = Timer()
hub = MSHub()

# Write your program here.
timer.reset()
hub.light_matrix.write(timer.now())

"""
    )


# - Key pressed
# Verified on Hardware
# TODO: Supper funcky that this currently doesn't work in MINDSTORMS, maybe only a mac thing :thinking:
def test_code_key_pressed():
    with raises(Exception) as _:
        helper("key_pressed", "Sensors")


# ---------- Operators ----------
# Verified on Hardware
def test_code_arithmetic():
    assert (
        helper("arithmetic", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 + (2.0 - (3.0 * (4.0 / 5.0)))))

"""
    )


# Verified on Hardware
def test_code_divide():
    assert (
        helper("divide", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 / 2.0))

"""
    )


# Verified on Hardware
def test_code_minus():
    assert (
        helper("minus", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 - 2.0))

"""
    )


# Verified on Hardware
def test_code_multiply():
    assert (
        helper("multiply", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 * 2.0))

"""
    )


# Verified on Hardware
def test_code_plus():
    assert (
        helper("plus", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
motor_a.run_for_rotations((1.0 + 2.0))

"""
    )


# Verified on Hardware
def test_code_arithmetic_variable():
    assert (
        helper("arithmetic_variable", "Operators")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable1 = 0.0
my_variable2 = 0.0
motor_a.run_for_rotations((my_variable1 + my_variable2))

"""
    )


# - Pick random number
# Verified on Hardware
def test_code_pick_random_number_base():
    assert (
        helper("pick_random_number_base", "Operators")
        == f"""{includes}from random import randint\n
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(randint(int(1.0), int(10.0)))

"""
    )


# Verified on Hardware
def test_code_pick_random_number_variable():
    assert (
        helper("pick_random_number_variable", "Operators")
        == f"""{includes}from random import randint\n
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 1.0
my_variable2 = 10.0
hub.light_matrix.write(randint(int(my_variable1), int(my_variable2)))

"""
    )


# - Less than
# Verified on Hardware
def test_code_less_than_base():
    assert (
        helper("less_than_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if (0.0 < 100.0):
\thub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_less_than_variable():
    assert (
        helper("less_than_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 1.0
my_variable2 = 10.0
if (my_variable1 < my_variable2):
\thub.light_matrix.write('Y')

"""
    )


# - Equal
# Verified on Hardware
def test_code_equal_base():
    assert (
        helper("equal_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if (100.0 == 100.0):
\thub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_equal_variable():
    assert (
        helper("equal_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 1.0
my_variable2 = 1.0
if (my_variable1 == my_variable2):
\thub.light_matrix.write('Y')

"""
    )


# - Greater than
# Verified on Hardware
def test_code_greater_than_base():
    assert (
        helper("greater_than_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if (110.0 > 100.0):
\thub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_greater_than_variable():
    assert (
        helper("greater_than_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 10.0
my_variable2 = 1.0
if (my_variable1 > my_variable2):
\thub.light_matrix.write('Y')

"""
    )


# - And
# Verified on Hardware
def test_code_and():
    assert (
        helper("and", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if ((1.0 == 1.0) and (2.0 == 2.0)):
\thub.light_matrix.write('Y')

"""
    )


# - Or
# Verified on Hardware
def test_code_or():
    assert (
        helper("or", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if ((0.0 == 1.0) or (1.0 == 1.0)):
\thub.light_matrix.write('Y')

"""
    )


# - Not
# Verified on Hardware
def test_code_not():
    assert (
        helper("not", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if not (0.0 == 1.0):
\thub.light_matrix.write('Y')

"""
    )


# - Is between
# Verified on Hardware
def test_code_is_between_base():
    assert (
        helper("is_between_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if -10.0 <= 0.0 <= 10.0:
\thub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_is_between_variable():
    assert (
        helper("is_between_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 0.0
my_variable2 = -10.0
my_variable3 = 10.0
if my_variable2 <= my_variable1 <= my_variable3:
\thub.light_matrix.write('Y')

"""
    )


# Join strings
# Verified on Hardware
def test_code_join_strings_base():
    assert (
        helper("join_strings_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write('Hello' + 'World')

"""
    )


# Verified on Hardware
def test_code_join_strings_variable():
    assert (
        helper("join_strings_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 'Hello'
my_variable2 = 'World'
hub.light_matrix.write(my_variable1 + my_variable2)

"""
    )


# - Letter of string
# Verified on Hardware
def test_code_letter_of_string_base():
    assert (
        helper("letter_of_string_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write('apple'[int(1.0) - 1])

"""
    )


# Verified on Hardware
def test_code_letter_of_string_variable():
    assert (
        helper("letter_of_string_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 1.0
my_variable2 = 'apple'
hub.light_matrix.write(my_variable2[int(my_variable1) - 1])

"""
    )


# - Length of string
# Verified on Hardware
def test_code_length_of_string_base():
    assert (
        helper("length_of_string_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(len('apple'))

"""
    )


# Verified on Hardware
def test_code_length_of_string_variable():
    assert (
        helper("length_of_string_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 'apple'
hub.light_matrix.write(len(my_variable))

"""
    )


# - String contains
# Verified on Hardware
def test_code_string_contains_base():
    assert (
        helper("string_contains_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
if 'a' in 'apple':
\thub.light_matrix.write('Y')

"""
    )


# Verified on Hardware
def test_code_string_contains_variable():
    assert (
        helper("string_contains_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 'apple'
my_variable2 = 'a'
if my_variable2 in my_variable1:
\thub.light_matrix.write('Y')

"""
    )


# - Mod
# Verified on Hardware
def test_code_mod_base():
    assert (
        helper("mod_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(4.0 % 2.0)

"""
    )


# Verified on Hardware
def test_code_mod_variable():
    assert (
        helper("mod_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 4.0
my_variable2 = 2.0
hub.light_matrix.write(my_variable1 % my_variable2)

"""
    )


# - Round
# Verified on Hardware
def test_code_round_base():
    assert (
        helper("round_base", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(int(4.2 + 0.5))

"""
    )


# Verified on Hardware
def test_code_round_variable():
    assert (
        helper("round_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable = 4.5
hub.light_matrix.write(int(my_variable + 0.5))

"""
    )


# - Math function
# 10
# Verified on Hardware
def test_code_math_function_10():
    assert (
        helper("math_function_10", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(pow(10, 1.0))

"""
    )


# abs
# Verified on Hardware
def test_code_math_function_abs():
    assert (
        helper("math_function_abs", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(abs(-1.0))

"""
    )


# acos
# Verified on Hardware
def test_code_math_function_acos():
    assert (
        helper("math_function_acos", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.acos(1.0))

"""
    )


# asin
# Verified on Hardware
def test_code_math_function_asin():
    assert (
        helper("math_function_asin", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.asin(1.0))

"""
    )


# atan
# Verified on Hardware
def test_code_math_function_atan():
    assert (
        helper("math_function_atan", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.atan(1.0))

"""
    )


# atan2
# Verified on Hardware
def test_code_math_function_atan2():
    assert (
        helper("math_function_atan2", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.atan2(0.0, 180.0))

"""
    )


# ceiling
# Verified on Hardware
def test_code_math_function_ceiling():
    assert (
        helper("math_function_ceiling", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.ceil(0.9))

"""
    )


# copysign
# Verified on Hardware
def test_code_math_function_copysign():
    assert (
        helper("math_function_copysign", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.copysign(1.0, -1.0))

"""
    )


# cos
# Verified on Hardware
def test_code_math_function_cos():
    assert (
        helper("math_function_cos", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.cos(180.0))

"""
    )


# e
# Verified on Hardware
def test_code_math_function_e():
    assert (
        helper("math_function_e", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(pow(math.e, 1.0))

"""
    )


# floor
# Verified on Hardware
def test_code_math_function_floor():
    assert (
        helper("math_function_floor", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.floor(1.9))

"""
    )


# hypot
# TODO: THis one is not found
def test_code_math_function_hypot():
    assert (
        helper("math_function_hypot", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.hypot(3.0, 4.0))

"""
    )


# ln
# Verified on Hardware
def test_code_math_function_ln():
    assert (
        helper("math_function_ln", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.log(1.0))

"""
    )


# log
# Verified on Hardware
def test_code_math_function_log():
    assert (
        helper("math_function_log", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.log2(1.0))

"""
    )


# max
# Verified on Hardware
def test_code_math_function_max():
    assert (
        helper("math_function_max", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(max(0.0, 1.0))

"""
    )


# min
# Verified on Hardware
def test_code_math_function_min():
    assert (
        helper("math_function_min", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(min(1.0, 10.0))

"""
    )


# pow
# Verified on Hardware
def test_code_math_function_pow():
    assert (
        helper("math_function_pow", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(pow(2.0, 3.0))

"""
    )


# sin
# Verified on Hardware
def test_code_math_function_sin():
    assert (
        helper("math_function_sin", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.sin(180.0))

"""
    )


# sqrt
# Verified on Hardware
def test_code_math_function_sqrt():
    assert (
        helper("math_function_sqrt", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.sqrt(4.0))

"""
    )


# tan
# Verified on Hardware
def test_code_math_function_tan():
    assert (
        helper("math_function_tan", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
hub.light_matrix.write(math.tan(180.0))

"""
    )


# variable
# Verified on Hardware
def test_code_math_function_variable():
    assert (
        helper("math_function_variable", "Operators")
        == f"""{includes}
# Create your objects here.
hub = MSHub()

# Write your program here.
my_variable1 = 1.0
my_variable2 = 10.0
hub.light_matrix.write(min(my_variable1, my_variable2))

"""
    )


# ---------- Variables ----------
# Verified on Hardware
def test_code_change_variable_by():
    assert (
        helper("change_variable_by", "Variables")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 0.0
my_variable += 1.0
motor_a.run_for_rotations(my_variable)

"""
    )


# Verified on Hardware
def test_code_variable_num():
    assert (
        helper("variable_num", "Variables")
        == f"""{includes}
# Create your objects here.
motor_a = Motor('A')

# Write your program here.
my_variable = 1.0
motor_a.run_for_rotations(my_variable)

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_variable_string():
    assert (
        helper("variable_string", "Variables")
        == f"""{includes}
# Create your objects here.

# Write your program here.
my_variable = 'A'
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_variable:
\tMotor(port).run_for_rotations(1.0)

"""
    )


# Verified on Hardware (Original code can't be replicated 100%)
def test_code_list():
    assert (
        helper("list", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('A')
my_list.append('B')
# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
for port in my_list:
\tMotor(port).run_for_rotations(1.0)

"""
    )


# Verified on Hardware
def test_code_add_item_to_list_base():
    assert (
        helper("add_item_to_list_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append('thing')

"""
    )


# Verified on Hardware
def test_code_add_item_to_list_int():
    assert (
        helper("add_item_to_list_int", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_list.append((1.0 + 2.0))

"""
    )


# TODO: Note that the list2 object is not made here, which might not be desirable, so fix eventually.
# Verified on Hardware
def test_code_add_item_to_list_list():
    assert (
        helper("add_item_to_list_list", "Variables")
        == f"""{includes}
# Create your objects here.
my_list1 = []

# Write your program here.
my_list1.append(my_list2)

"""
    )


# Verified on Hardware
def test_code_item_to_list_variable():
    assert (
        helper("add_item_to_list_variable", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []

# Write your program here.
my_variable = 'A'
my_list.append(my_variable)

"""
    )


# - Delete item in list
# Verified on Hardware
def test_code_delete_item_in_list_base():
    assert (
        helper("delete_item_in_list_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
del my_list[int(2.0) - 1]  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list)

"""
    )


# Verified on Hardware
def test_code_delete_item_in_list_variable():
    assert (
        helper("delete_item_in_list_variable", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 1.0
my_list.append('a')
my_list.append('b')
del my_list[int(my_variable) - 1]  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list)

"""
    )


# - Delete all items in list
# Verified on Hardware
def test_code_delete_all_items_in_list():
    assert (
        helper("delete_all_items_in_list", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
my_list.clear()
hub.light_matrix.write(len(my_list))

"""
    )


# - Insert item at index
# Verified on Hardware
def test_code_insert_item_at_index_base():
    assert (
        helper("insert_item_at_index_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
my_list.insert(int(1.0) - 1, 'c')  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(1.0) - 1])

"""
    )


# Verified on Hardware
def test_code_insert_item_at_index_variable_index():
    assert (
        helper("insert_item_at_index_variable_index", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 2.0
my_list.append('a')
my_list.append('b')
my_list.insert(int(my_variable) - 1, 'c')  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(2.0) - 1])

"""
    )


# Verified on Hardware
def test_code_insert_item_at_index_variable_item():
    assert (
        helper("insert_item_at_index_variable_item", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 'c'
my_list.append('a')
my_list.append('b')
my_list.insert(int(1.0) - 1, my_variable)  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(1.0) - 1])

"""
    )


# - Replace item at index
# Verified on Hardware
def test_code_replace_item_at_index_base():
    assert (
        helper("replace_item_at_index_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list[int(1.0) - 1] = 'c'  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(1.0) - 1])

"""
    )


# Verified on Hardware
def test_code_replace_item_at_index_variable_index():
    assert (
        helper("replace_item_at_index_variable_index", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 2.0
my_list.append('a')
my_list.append('b')
my_list[int(my_variable) - 1] = 'c'  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(2.0) - 1])

"""
    )


# Verified on Hardware
def test_code_replace_item_at_index_variable_value():
    assert (
        helper("replace_item_at_index_variable_value", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 'c'
my_list.append('a')
my_list[int(1.0) - 1] = my_variable  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.
hub.light_matrix.write(my_list[int(1.0) - 1])

"""
    )


# - Item at Index
# Verified on Hardware
def test_code_item_at_index_base():
    assert (
        helper("item_at_index_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
hub.light_matrix.write(my_list[int(2.0) - 1])

"""
    )


# Verified on Hardware
def test_code_item_at_index_variable():
    assert (
        helper("item_at_index_variable", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 1.0
my_list.append('a')
my_list.append('b')
hub.light_matrix.write(my_list[int(my_variable) - 1])

"""
    )


# - Index of item
# Verified on Hardware
def test_code_index_of_item_base():
    assert (
        helper("index_of_item_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
hub.light_matrix.write(my_list.index('b') + 1)

"""
    )


# Verified on Hardware
def test_code_index_of_item_variable():
    assert (
        helper("index_of_item_variable", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 'a'
my_list.append('a')
my_list.append('b')
hub.light_matrix.write(my_list.index(my_variable) + 1)

"""
    )


# - Length of list
# Verified on Hardware
def test_code_length_of_list():
    assert (
        helper("length_of_list", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
my_list.append('b')
hub.light_matrix.write(len(my_list))

"""
    )


# - List contains
# Verified on Hardware
def test_code_list_contains_base():
    assert (
        helper("list_contains_base", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_list.append('a')
if 'a' in my_list:
\thub.light_matrix.write('a')

"""
    )


# Verified on Hardware
def test_code_list_contains_variable():
    assert (
        helper("list_contains_variable", "Variables")
        == f"""{includes}
# Create your objects here.
my_list = []
hub = MSHub()

# Write your program here.
my_variable = 'a'
my_list.append('b')
if my_variable in my_list:
\thub.light_matrix.write('a')

"""
    )
