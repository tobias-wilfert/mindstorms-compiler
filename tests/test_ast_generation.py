# Test to check that the AST is generated correctly.

from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


def ast_helper(filename: str, directory: str = ".") -> str:
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
    return abstract_syntax_tree.tree_representation()


# ---------- Base ----------
def test_ast_empty():
    assert (
        ast_helper("empty")
        == """digraph {rankdir="TB"

}"""
    )


# ---------- Events ----------
def test_ast_when_program_starts():
    assert (
        ast_helper("when_program_starts", "Events")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
}"""
    )


# ---------- Motors ----------
# - Run Motor for duration
def test_ast_run_motor_for_duration_base():
    assert (
        ast_helper("run_motor_for_duration_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_counterclockwise():
    assert (
        ast_helper("run_motor_for_duration_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.COUNTERCLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_degrees():
    assert (
        ast_helper("run_motor_for_duration_degrees", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.DEGREES')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_multiple_motors():
    assert (
        ast_helper("run_motor_for_duration_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A', 'E']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_multiple_motors3():
    assert (
        ast_helper("run_motor_for_duration_multiple_motors3", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A', 'B', 'C']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_all_motors():
    assert (
        ast_helper("run_motor_for_duration_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_seconds():
    assert (
        ast_helper("run_motor_for_duration_seconds", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.SECONDS')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_value_node():
    assert (
        ast_helper("run_motor_for_duration_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Motor Go to Position
def test_ast_motor_go_to_position_base():
    assert (
        ast_helper("motor_go_to_position_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_clockwise():
    assert (
        ast_helper("motor_go_to_position_clockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.CLOCKWISE')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_counterclockwise():
    assert (
        ast_helper("motor_go_to_position_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.COUNTERCLOCKWISE')"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_multiple_motors():
    assert (
        ast_helper("motor_go_to_position_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListNode('['A', 'B']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_value_node():
    assert (
        ast_helper("motor_go_to_position_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Start Motor
def test_ast_start_motor_base():
    assert (
        ast_helper("start_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_all_motors():
    assert (
        ast_helper("start_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_multiple_motors():
    assert (
        ast_helper("start_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListNode('['A', 'B']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_counterclockwise():
    assert (
        ast_helper("start_motor_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.COUNTERCLOCKWISE')"]
2 [label="ListNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


# - Stop Motor
def test_ast_stop_motor_base():
    assert (
        ast_helper("stop_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_stop_motor_all_motors():
    assert (
        ast_helper("stop_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_stop_motor_multiple_motors():
    assert (
        ast_helper("stop_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListNode('['A', 'B']')"]
0 -> 1
1 -> 2}"""
    )


# - Set Motor Speed
def test_ast_set_motor_speed_base():
    assert (
        ast_helper("set_motor_speed_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListNode('['A']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_all_motors():
    assert (
        ast_helper("set_motor_speed_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_multiple_motors():
    assert (
        ast_helper("set_motor_speed_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListNode('['A', 'B']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_value_node():
    assert (
        ast_helper("set_motor_speed_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(25.0)"]
5 [label="NumericalNode(50.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# ---------- Operators ----------
def test_ast_arithmetic():
    assert (
        ast_helper("arithmetic", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="ArithmeticalNode(op:'Operation.MINUS')"]
6 [label="NumericalNode(2.0)"]
7 [label="ArithmeticalNode(op:'Operation.MULTIPLY')"]
8 [label="NumericalNode(3.0)"]
9 [label="ArithmeticalNode(op:'Operation.DIVIDE')"]
10 [label="NumericalNode(4.0)"]
11 [label="NumericalNode(5.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9
9 -> 10
9 -> 11}"""
    )


def test_ast_divide():
    assert (
        ast_helper("divide", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.DIVIDE')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_minus():
    assert (
        ast_helper("minus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.MINUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_multiply():
    assert (
        ast_helper("multiply", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.MULTIPLY')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_plus():
    assert (
        ast_helper("plus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# ---------- Variables ----------
def test_ast_change_variable_by():
    assert (
        ast_helper("change_variable_by", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="ChangeVariableByNode(variable:'my_variable')"]
4 [label="NumericalNode(1.0)"]
5 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
6 [label="ListNode('['A']')"]
7 [label="Variable(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7}"""
    )


def test_ast_variable_num():
    assert (
        ast_helper("variable_num", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(1.0)"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListNode('['A']')"]
5 [label="Variable(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_variable_string():
    assert (
        ast_helper("variable_string", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="Variable(name:'my_variable')"]
5 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )
