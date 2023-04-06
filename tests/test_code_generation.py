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
motor_a.run_for_degrees(int(1.0))  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int(0.0), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int(0.0), 'clockwise')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int(0.0), 'counterclockwise')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int(0.0), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.
motor_b.run_to_position(int(0.0), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int((1.0 + 2.0)), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
\tMotor(port).run_to_position(int(0.0), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
\tMotor(port).run_to_position(int(0.0), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.run_to_position(int(my_variable), 'shortest path')  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_b.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_c.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_d.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_e.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_f.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.
motor_b.set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.set_default_speed(int((25.0 + 50.0)))  # Note: This methods expects an integer so wee need to convert the value.

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
\tMotor(port).set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.

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
\tMotor(port).set_default_speed(int(75.0))  # Note: This methods expects an integer so wee need to convert the value.

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
motor_a.set_default_speed(int(my_variable))  # Note: This methods expects an integer so wee need to convert the value.

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
