# Test to check that the Code is generated correctly

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
    visitor = Visitor()
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
