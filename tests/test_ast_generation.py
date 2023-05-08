# Test to check that the AST is generated correctly.

from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


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
    return abstract_syntax_tree.tree_representation()


# ---------- Base ----------
def test_ast_empty():
    assert (
        helper("empty")
        == """digraph {rankdir="TB"

}"""
    )


# ---------- Events ----------
def test_ast_when_program_starts():
    assert (
        helper("when_program_starts", "Events")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
}"""
    )


# ---------- Motors ----------
# - Run Motor for duration
def test_ast_run_motor_for_duration_base():
    assert (
        helper("run_motor_for_duration_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_counterclockwise():
    assert (
        helper("run_motor_for_duration_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.COUNTERCLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_degrees():
    assert (
        helper("run_motor_for_duration_degrees", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.DEGREES')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_multiple_motors():
    assert (
        helper("run_motor_for_duration_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A', 'E']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_multiple_motors3():
    assert (
        helper("run_motor_for_duration_multiple_motors3", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A', 'B', 'C']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_all_motors():
    assert (
        helper("run_motor_for_duration_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_seconds():
    assert (
        helper("run_motor_for_duration_seconds", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.SECONDS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_run_motor_for_duration_value_node():
    assert (
        helper("run_motor_for_duration_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_run_motor_for_duration_port_list():
    assert (
        helper("run_motor_for_duration_port_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="VariableNode(name:'my_list')"]
5 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_run_motor_for_duration_port_variable():
    assert (
        helper("run_motor_for_duration_port_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_run_motor_for_duration_value_variable():
    assert (
        helper("run_motor_for_duration_value_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Motor Go to Position
def test_ast_motor_go_to_position_base():
    assert (
        helper("motor_go_to_position_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_clockwise():
    assert (
        helper("motor_go_to_position_clockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.CLOCKWISE')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_counterclockwise():
    assert (
        helper("motor_go_to_position_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.COUNTERCLOCKWISE')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_multiple_motors():
    assert (
        helper("motor_go_to_position_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_motor_go_to_position_value_node():
    assert (
        helper("motor_go_to_position_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_motor_go_to_position_port_list():
    assert (
        helper("motor_go_to_position_port_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
4 [label="VariableNode(name:'my_list')"]
5 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_motor_go_to_position_port_variable():
    assert (
        helper("motor_go_to_position_port_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_motor_go_to_position_value_variable():
    assert (
        helper("motor_go_to_position_value_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="MotorGoToPositionNode(direction:'GoDirection.SHORTEST')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Start Motor
def test_ast_start_motor_base():
    assert (
        helper("start_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_all_motors():
    assert (
        helper("start_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListLiteralNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_multiple_motors():
    assert (
        helper("start_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
2 [label="ListLiteralNode('['A', 'B']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_counterclockwise():
    assert (
        helper("start_motor_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(direction:'TurnDirection.COUNTERCLOCKWISE')"]
2 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_start_motor_port_list():
    assert (
        helper("start_motor_port_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
4 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_start_motor_port_variable():
    assert (
        helper("start_motor_port_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="StartMotorNode(direction:'TurnDirection.CLOCKWISE')"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Stop Motor
def test_ast_stop_motor_base():
    assert (
        helper("stop_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_stop_motor_all_motors():
    assert (
        helper("stop_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListLiteralNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_stop_motor_multiple_motors():
    assert (
        helper("stop_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_stop_motor_port_list():
    assert (
        helper("stop_motor_port_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="StopMotorNode"]
4 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_stop_motor_port_variable():
    assert (
        helper("stop_motor_port_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="StopMotorNode"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Set Motor Speed
def test_ast_set_motor_speed_base():
    assert (
        helper("set_motor_speed_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListLiteralNode('['A']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_all_motors():
    assert (
        helper("set_motor_speed_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListLiteralNode('['A', 'B', 'C', 'D', 'E', 'F']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_multiple_motors():
    assert (
        helper("set_motor_speed_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_motor_speed_value_node():
    assert (
        helper("set_motor_speed_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMotorSpeedNode"]
2 [label="ListLiteralNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(25.0)"]
5 [label="NumericalNode(50.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_set_motor_speed_list():
    assert (
        helper("set_motor_speed_port_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="SetMotorSpeedNode"]
4 [label="VariableNode(name:'my_list')"]
5 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_set_motor_speed_port_variable():
    assert (
        helper("set_motor_speed_port_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="SetMotorSpeedNode"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="NumericalNode(75.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_set_motor_speed_value_variable():
    assert (
        helper("set_motor_speed_value_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(75.0)"]
3 [label="SetMotorSpeedNode"]
4 [label="ListLiteralNode('['A']')"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# Motor Position
def test_ast_motor_position_base():
    assert (
        helper("motor_position_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="MotorPositionNode"]
4 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# TODO: Need to check how this would even be handled ATM.
def test_ast_motor_position_list():
    assert (
        helper("motor_position_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="MotorPositionNode"]
6 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_motor_position_variable():
    assert (
        helper("motor_position_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="MotorPositionNode"]
6 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


# Motor Speed
def test_ast_motor_speed_base():
    assert (
        helper("motor_speed_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="MotorSpeedNode"]
4 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# TODO: Need to check how this would even be handled ATM.
def test_ast_motor_speed_list():
    assert (
        helper("motor_speed_list", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="MotorSpeedNode"]
6 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_motor_speed_variable():
    assert (
        helper("motor_speed_variable", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="MotorSpeedNode"]
6 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


# ---------- Movement ----------
# - Move for duration
def test_ast_move_for_duration_backwards():
    assert (
        helper("move_for_duration_backwards", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.BACK', unit:'MovementUnit.CM')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_base():
    assert (
        helper("move_for_duration_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_clockwise():
    assert (
        helper("move_for_duration_clockwise", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.CLOCKWISE', unit:'MovementUnit.CM')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_counterclockwise():
    assert (
        helper("move_for_duration_counterclockwise", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.COUNTERCLOCKWISE', unit:'MovementUnit.CM')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_degrees():
    assert (
        helper("move_for_duration_degrees", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.DEGREES')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_inches():
    assert (
        helper("move_for_duration_inches", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.INCHES')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_rotations():
    assert (
        helper("move_for_duration_rotations", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.ROTATIONS')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_seconds():
    assert (
        helper("move_for_duration_seconds", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.SECONDS')"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_move_for_duration_value_variable():
    assert (
        helper("move_for_duration_value_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(10.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
6 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


# - Move with Steering
def test_ast_move_with_steering_base():
    assert (
        helper("move_with_steering_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveWithSteeringNode(unit:'MovementUnit.CM')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_move_with_steering_degrees():
    assert (
        helper("move_with_steering_degrees", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveWithSteeringNode(unit:'MovementUnit.DEGREES')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_move_with_steering_inches():
    assert (
        helper("move_with_steering_inches", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveWithSteeringNode(unit:'MovementUnit.INCHES')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_move_with_steering_rotations():
    assert (
        helper("move_with_steering_rotations", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveWithSteeringNode(unit:'MovementUnit.ROTATIONS')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_move_with_steering_seconds():
    assert (
        helper("move_with_steering_seconds", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="MoveWithSteeringNode(unit:'MovementUnit.SECONDS')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_move_with_steering_steering_variable():
    assert (
        helper("move_with_steering_steering_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="MoveWithSteeringNode(unit:'MovementUnit.CM')"]
6 [label="VariableNode(name:'my_variable')"]
7 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7}"""
    )


def test_ast_move_with_steering_value_variable():
    assert (
        helper("move_with_steering_value_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(10.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="MoveWithSteeringNode(unit:'MovementUnit.CM')"]
6 [label="NumericalNode(0.0)"]
7 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7}"""
    )


# - Start Moving with Steering
def test_ast_start_moving_with_steering_base():
    assert (
        helper("start_moving_with_steering_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="StartMowingWithSteeringNode"]
4 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_start_moving_with_steering_variable():
    assert (
        helper("start_moving_with_steering_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="StartMowingWithSteeringNode"]
6 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


# - Stop Moving
def test_ast_stop_moving():
    assert (
        helper("stop_moving", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="StartMowingWithSteeringNode"]
4 [label="NumericalNode(0.0)"]
5 [label="StopMovingNode"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Set Movement Speed
def test_ast_set_movement_speed_base():
    assert (
        helper("set_movement_speed_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="SetMovementSpeedNode"]
4 [label="NumericalNode(50.0)"]
5 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
6 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_set_movement_speed_value_variable():
    assert (
        helper("set_movement_speed_value_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(10.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="SetMovementSpeedNode"]
6 [label="VariableNode(name:'my_variable')"]
7 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
8 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8}"""
    )


# - Set Movement Motors
def test_ast_set_movement_motors_base():
    assert (
        helper("set_movement_motors_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_set_movement_motors_list():
    assert (
        helper("set_movement_motors_list", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('B')"]
5 [label="SetMovementMotorsNode"]
6 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_set_movement_motors_variable():
    assert (
        helper("set_movement_motors_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('AB')"]
3 [label="SetMovementMotorsNode"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Set Motor rotation
def test_ast_set_motor_rotation_base():
    assert (
        helper("set_motor_rotation_base", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="SetMotorRotationNode(unit:'RotationUnit.CM')"]
4 [label="NumericalNode(17.5)"]
5 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
6 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_set_motor_rotation_inches():
    assert (
        helper("set_motor_rotation_inches", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetMovementMotorsNode"]
2 [label="ListLiteralNode('['A', 'B']')"]
3 [label="SetMotorRotationNode(unit:'RotationUnit.INCHES')"]
4 [label="NumericalNode(17.5)"]
5 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
6 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


def test_ast_set_motor_rotation_value_variable():
    assert (
        helper("set_motor_rotation_value_variable", "Movement")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(10.0)"]
3 [label="SetMovementMotorsNode"]
4 [label="ListLiteralNode('['A', 'B']')"]
5 [label="SetMotorRotationNode(unit:'RotationUnit.CM')"]
6 [label="VariableNode(name:'my_variable')"]
7 [label="MoveForDurationNode(direction:'MovementDirection.FORWARD', unit:'MovementUnit.CM')"]
8 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8}"""
    )


# ---------- Light ----------
# - Start Animation
def test_ast_start_animation_base():
    assert (
        helper("start_animation_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_start_animation_custom():
    assert (
        helper("start_animation_custom", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


# - Play Animation until done
def test_ast_play_animation_until_done_base():
    assert (
        helper("play_animation_until_done_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_play_animation_until_done_custom():
    assert (
        helper("play_animation_until_done_custom", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


# - Turn on for duration
def test_ast_turn_on_for_duration_base():
    assert (
        helper("turn_on_for_duration_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="TurnOnForDurationNode(image: '9909999099000009000909990')"]
2 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_turn_on_for_duration_custom():
    assert (
        helper("turn_on_for_duration_custom", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="TurnOnForDurationNode(image: '0000009990099900999000000')"]
2 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_turn_on_for_duration_variable():
    assert (
        helper("turn_on_for_duration_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(3.0)"]
3 [label="TurnOnForDurationNode(image: '9909999099000009000909990')"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Turn on
def test_ast_turn_on_base():
    assert (
        helper("turn_on_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="TurnOnNode(image: '9909999099000009000909990')"]
0 -> 1}"""
    )


def test_ast_turn_on_custom():
    assert (
        helper("turn_on_custom", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="TurnOnNode(image: '0000009990099900999000000')"]
0 -> 1}"""
    )


# - Write
def test_ast_write_base():
    assert (
        helper("write_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="LiteralNode('Hello World')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_write_variable():
    assert (
        helper("write_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('Hello World')"]
3 [label="WriteNode"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Turn off
def test_ast_turn_off_pixels():
    assert (
        helper("turn_off_pixels", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="TurnOffPixelsNode"]
0 -> 1}"""
    )


# - Set pixel brightness
def test_ast_set_pixel_brightness_base():
    assert (
        helper("set_pixel_brightness_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetPixelBrightnessNode"]
2 [label="NumericalNode(75.0)"]
3 [label="TurnOnNode(image: '9909999099000009000909990')"]
0 -> 1
1 -> 2
1 -> 3}"""
    )


def test_ast_set_pixel_brightness_variable():
    assert (
        helper("set_pixel_brightness_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(50.0)"]
3 [label="SetPixelBrightnessNode"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="TurnOnNode(image: '9909999099000009000909990')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


# - Set pixel
def test_ast_set_pixel_base():
    assert (
        helper("set_pixel_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetPixelNode"]
2 [label="NumericalNode(1.0)"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(100.0)"]
0 -> 1
1 -> 2
1 -> 3
1 -> 4}"""
    )


def test_ast_set_pixel_variable():
    assert (
        helper("set_pixel_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(50.0)"]
3 [label="SetPixelNode"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(1.0)"]
6 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
3 -> 6}"""
    )


def test_ast_set_pixel_x_value_variable():
    assert (
        helper("set_pixel_x_value_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(2.0)"]
3 [label="SetPixelNode"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="NumericalNode(1.0)"]
6 [label="NumericalNode(100.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
3 -> 6}"""
    )


def test_ast_set_pixel_y_value_variable():
    assert (
        helper("set_pixel_y_value_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(2.0)"]
3 [label="SetPixelNode"]
4 [label="NumericalNode(1.0)"]
5 [label="VariableNode(name:'my_variable')"]
6 [label="NumericalNode(100.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
3 -> 6}"""
    )


# - Rotate Orientation
def test_ast_rotate_orientation_clockwise():
    assert (
        helper("rotate_orientation_clockwise", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_rotate_orientation_counterclockwise():
    assert (
        helper("rotate_orientation_counterclockwise", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


# - Set Orientation
def test_ast_set_orientation_upright():
    assert (
        helper("set_orientation_upright", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_set_orientation_upsidedown():
    assert (
        helper("set_orientation_upsidedown", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_set_orientation_left():
    assert (
        helper("set_orientation_left", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


def test_ast_set_orientation_right():
    assert (
        helper("set_orientation_right", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="CommentNode('# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.')"]
0 -> 1}"""
    )


# - Set Center button
def test_ast_set_center_button_red():
    assert (
        helper("set_center_button_red", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.RED')"]
0 -> 1}"""
    )


def test_ast_set_center_button_yellow():
    assert (
        helper("set_center_button_yellow", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.YELLOW')"]
0 -> 1}"""
    )


def test_ast_set_center_button_green():
    assert (
        helper("set_center_button_green", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.GREEN')"]
0 -> 1}"""
    )


def test_ast_set_center_button_cyan():
    assert (
        helper("set_center_button_cyan", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.CYAN')"]
0 -> 1}"""
    )


def test_ast_set_center_button_azure():
    assert (
        helper("set_center_button_azure", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.AZURE')"]
0 -> 1}"""
    )


def test_ast_set_center_button_pink():
    assert (
        helper("set_center_button_pink", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.PINK')"]
0 -> 1}"""
    )


def test_ast_set_center_button_white():
    assert (
        helper("set_center_button_white", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.WHITE')"]
0 -> 1}"""
    )


def test_ast_set_center_button_black():
    assert (
        helper("set_center_button_black", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetCenterButtonNode(color: 'CenterButtonColor.BLACK')"]
0 -> 1}"""
    )


# -Light up distance sensor
def test_ast_light_up_distance_sensor_base():
    assert (
        helper("light_up_distance_sensor_base", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="LightUpDistanceSensorNode(pattern: '100 100 100 100')"]
2 [label="ListLiteralNode('['A']')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_light_up_distance_sensor_port_list():
    assert (
        helper("light_up_distance_sensor_port_list", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="LightUpDistanceSensorNode(pattern: '100 100 100 100')"]
4 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


def test_ast_light_up_distance_sensor_port_variable():
    assert (
        helper("light_up_distance_sensor_port_variable", "Light")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="LightUpDistanceSensorNode(pattern: '100 100 100 100')"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# ---------- Operators ----------
def test_ast_arithmetic():
    assert (
        helper("arithmetic", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
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
        helper("divide", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
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
        helper("minus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
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
        helper("multiply", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
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
        helper("plus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
2 [label="ListLiteralNode('['A']')"]
3 [label="ArithmeticalNode(op:'Operation.PLUS')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_arithmetic_variable():
    assert (
        helper("arithmetic_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(0.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(0.0)"]
5 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
6 [label="ListLiteralNode('['A']')"]
7 [label="ArithmeticalNode(op:'Operation.PLUS')"]
8 [label="VariableNode(name:'my_variable1')"]
9 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9}"""
    )


# - Pick random number
def test_ast_pick_random_number_base():
    assert (
        helper("pick_random_number_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="PickRandomNumberNode"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_pick_random_number_variable():
    assert (
        helper("pick_random_number_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(1.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(10.0)"]
5 [label="WriteNode"]
6 [label="PickRandomNumberNode"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8}"""
    )


# - Less than
def test_ast_less_than_base():
    assert (
        helper("less_than_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="ComparisonNode(op:'ComparisonOperator.LESS')"]
3 [label="NumericalNode(0.0)"]
4 [label="NumericalNode(100.0)"]
5 [label="WriteNode"]
6 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
1 -> 5
5 -> 6}"""
    )


def test_ast_less_than_variable():
    assert (
        helper("less_than_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(1.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(10.0)"]
5 [label="IfThenNode"]
6 [label="ComparisonNode(op:'ComparisonOperator.LESS')"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8
5 -> 9
9 -> 10}"""
    )


# - Equal
def test_ast_equal_base():
    assert (
        helper("equal_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
3 [label="NumericalNode(100.0)"]
4 [label="NumericalNode(100.0)"]
5 [label="WriteNode"]
6 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
1 -> 5
5 -> 6}"""
    )


def test_ast_equal_variable():
    assert (
        helper("equal_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(1.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(1.0)"]
5 [label="IfThenNode"]
6 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8
5 -> 9
9 -> 10}"""
    )


# - Greater than
def test_ast_greater_than_base():
    assert (
        helper("greater_than_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="ComparisonNode(op:'ComparisonOperator.GREATER')"]
3 [label="NumericalNode(110.0)"]
4 [label="NumericalNode(100.0)"]
5 [label="WriteNode"]
6 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
1 -> 5
5 -> 6}"""
    )


def test_ast_greater_than_variable():
    assert (
        helper("greater_than_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(10.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(1.0)"]
5 [label="IfThenNode"]
6 [label="ComparisonNode(op:'ComparisonOperator.GREATER')"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8
5 -> 9
9 -> 10}"""
    )


# - And
def test_ast_and():
    assert (
        helper("and", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="ComparisonNode(op:'ComparisonOperator.AND')"]
3 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
4 [label="NumericalNode(1.0)"]
5 [label="NumericalNode(1.0)"]
6 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
7 [label="NumericalNode(2.0)"]
8 [label="NumericalNode(2.0)"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
3 -> 4
3 -> 5
2 -> 6
6 -> 7
6 -> 8
1 -> 9
9 -> 10}"""
    )


# - Or
def test_ast_or():
    assert (
        helper("or", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="ComparisonNode(op:'ComparisonOperator.OR')"]
3 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(1.0)"]
6 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
7 [label="NumericalNode(1.0)"]
8 [label="NumericalNode(1.0)"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
3 -> 4
3 -> 5
2 -> 6
6 -> 7
6 -> 8
1 -> 9
9 -> 10}"""
    )


# - Not
def test_ast_not():
    assert (
        helper("not", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="NotNode"]
3 [label="ComparisonNode(op:'ComparisonOperator.EQUAL')"]
4 [label="NumericalNode(0.0)"]
5 [label="NumericalNode(1.0)"]
6 [label="WriteNode"]
7 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
3 -> 4
3 -> 5
1 -> 6
6 -> 7}"""
    )


# - Is between
def test_ast_is_between_base():
    assert (
        helper("is_between_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="IsBetweenNode"]
3 [label="NumericalNode(0.0)"]
4 [label="NumericalNode(-10.0)"]
5 [label="NumericalNode(10.0)"]
6 [label="WriteNode"]
7 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
2 -> 5
1 -> 6
6 -> 7}"""
    )


def test_ast_is_between_variable():
    assert (
        helper("is_between_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(0.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(-10.0)"]
5 [label="SetVariableToNode(variable:'my_variable3')"]
6 [label="NumericalNode(10.0)"]
7 [label="IfThenNode"]
8 [label="IsBetweenNode"]
9 [label="VariableNode(name:'my_variable1')"]
10 [label="VariableNode(name:'my_variable2')"]
11 [label="VariableNode(name:'my_variable3')"]
12 [label="WriteNode"]
13 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
8 -> 9
8 -> 10
8 -> 11
7 -> 12
12 -> 13}"""
    )


# Join strings
def test_ast_join_strings_base():
    assert (
        helper("join_strings_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="JoinStringsNode"]
3 [label="LiteralNode('Hello')"]
4 [label="LiteralNode('World')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_join_strings_variable():
    assert (
        helper("join_strings_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="LiteralNode('Hello')"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="LiteralNode('World')"]
5 [label="WriteNode"]
6 [label="JoinStringsNode"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8}"""
    )


# - Letter of string
def test_ast_letter_of_string_base():
    assert (
        helper("letter_of_string_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="LetterOfStringNode"]
3 [label="NumericalNode(1.0)"]
4 [label="LiteralNode('apple')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_letter_of_string_variable():
    assert (
        helper("letter_of_string_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(1.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="LiteralNode('apple')"]
5 [label="WriteNode"]
6 [label="LetterOfStringNode"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8}"""
    )


# - Length of string
def test_ast_length_of_string_base():
    assert (
        helper("length_of_string_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="LengthOfStringNode"]
3 [label="LiteralNode('apple')"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


def test_ast_length_of_string_variable():
    assert (
        helper("length_of_string_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('apple')"]
3 [label="WriteNode"]
4 [label="LengthOfStringNode"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
4 -> 5}"""
    )


# - String contains
def test_ast_string_contains_base():
    assert (
        helper("string_contains_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="IfThenNode"]
2 [label="StringContainsNode"]
3 [label="LiteralNode('apple')"]
4 [label="LiteralNode('a')"]
5 [label="WriteNode"]
6 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
1 -> 5
5 -> 6}"""
    )


def test_ast_string_contains_variable():
    assert (
        helper("string_contains_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="LiteralNode('apple')"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="LiteralNode('a')"]
5 [label="IfThenNode"]
6 [label="StringContainsNode"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
9 [label="WriteNode"]
10 [label="LiteralNode('Y')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8
5 -> 9
9 -> 10}"""
    )


# - Mod
def test_ast_mod_base():
    assert (
        helper("mod_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="ModNode"]
3 [label="NumericalNode(4.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_mod_variable():
    assert (
        helper("mod_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(4.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(2.0)"]
5 [label="WriteNode"]
6 [label="ModNode"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8}"""
    )


# - Round
def test_ast_round_base():
    assert (
        helper("round_base", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="RoundNode"]
3 [label="NumericalNode(4.2)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


def test_ast_round_variable():
    assert (
        helper("round_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(4.5)"]
3 [label="WriteNode"]
4 [label="RoundNode"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
4 -> 5}"""
    )


# - Math function
# 10
def test_ast_math_function_10():
    assert (
        helper("math_function_10", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.TEN')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# abs
def test_ast_math_function_abs():
    assert (
        helper("math_function_abs", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.ABS')"]
3 [label="NumericalNode(-1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# acos
def test_ast_math_function_acos():
    assert (
        helper("math_function_acos", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.ACOS')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# asin
def test_ast_math_function_asin():
    assert (
        helper("math_function_asin", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.ASIN')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# atan
def test_ast_math_function_atan():
    assert (
        helper("math_function_atan", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.ATAN')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# atan2
def test_ast_math_function_atan2():
    assert (
        helper("math_function_atan2", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.ATAN2')"]
3 [label="NumericalNode(0.0)"]
4 [label="NumericalNode(180.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# ceiling
def test_ast_math_function_ceiling():
    assert (
        helper("math_function_ceiling", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.CEIL')"]
3 [label="NumericalNode(0.9)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# copysign
def test_ast_math_function_copysign():
    assert (
        helper("math_function_copysign", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.COPYSIGN')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(-1.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# cos
def test_ast_math_function_cos():
    assert (
        helper("math_function_cos", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.COS')"]
3 [label="NumericalNode(180.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# e
def test_ast_math_function_e():
    assert (
        helper("math_function_e", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.E')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# floor
def test_ast_math_function_floor():
    assert (
        helper("math_function_floor", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.FLOOR')"]
3 [label="NumericalNode(1.9)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# hypot
def test_ast_math_function_hypot():
    assert (
        helper("math_function_hypot", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.HYPOT')"]
3 [label="NumericalNode(3.0)"]
4 [label="NumericalNode(4.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# ln
def test_ast_math_function_ln():
    assert (
        helper("math_function_ln", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.LN')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# log
def test_ast_math_function_log():
    assert (
        helper("math_function_log", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.LOG')"]
3 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# max
def test_ast_math_function_max():
    assert (
        helper("math_function_max", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.MAX')"]
3 [label="NumericalNode(0.0)"]
4 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# min
def test_ast_math_function_min():
    assert (
        helper("math_function_min", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.MIN')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(10.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# pow
def test_ast_math_function_pow():
    assert (
        helper("math_function_pow", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="BinaryMathFunction(function:'BinaryFunction.POW')"]
3 [label="NumericalNode(2.0)"]
4 [label="NumericalNode(3.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# sin
def test_ast_math_function_sin():
    assert (
        helper("math_function_sin", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.SIN')"]
3 [label="NumericalNode(180.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# sqrt
def test_ast_math_function_sqrt():
    assert (
        helper("math_function_sqrt", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.SQRT')"]
3 [label="NumericalNode(4.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# tan
def test_ast_math_function_tan():
    assert (
        helper("math_function_tan", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="WriteNode"]
2 [label="UnaryMathFunctionNode(function:'UnaryFunction.TAN')"]
3 [label="NumericalNode(180.0)"]
0 -> 1
1 -> 2
2 -> 3}"""
    )


# variable
def test_ast_math_function_variable():
    assert (
        helper("math_function_variable", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable1')"]
2 [label="NumericalNode(1.0)"]
3 [label="SetVariableToNode(variable:'my_variable2')"]
4 [label="NumericalNode(10.0)"]
5 [label="WriteNode"]
6 [label="BinaryMathFunction(function:'BinaryFunction.MIN')"]
7 [label="VariableNode(name:'my_variable1')"]
8 [label="VariableNode(name:'my_variable2')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
6 -> 8}"""
    )


# ---------- Variables ----------
def test_ast_change_variable_by():
    assert (
        helper("change_variable_by", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(0.0)"]
3 [label="ChangeVariableByNode(variable:'my_variable')"]
4 [label="NumericalNode(1.0)"]
5 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
6 [label="ListLiteralNode('['A']')"]
7 [label="VariableNode(name:'my_variable')"]
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
        helper("variable_num", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(1.0)"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="ListLiteralNode('['A']')"]
5 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_variable_string():
    assert (
        helper("variable_string", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
4 [label="VariableNode(name:'my_variable')"]
5 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5}"""
    )


def test_ast_list():
    assert (
        helper("list", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('A')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('B')"]
5 [label="RunMotorForDurationNode(direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS')"]
6 [label="VariableNode(name:'my_list')"]
7 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7}"""
    )


def test_ast_add_item_to_list_base():
    assert (
        helper("add_item_to_list_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('thing')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_add_item_to_list_int():
    assert (
        helper("add_item_to_list_int", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="ArithmeticalNode(op:'Operation.PLUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_add_item_to_list_list():
    assert (
        helper("add_item_to_list_list", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list1')"]
2 [label="VariableNode(name:'my_list2')"]
0 -> 1
1 -> 2}"""
    )


def test_ast_item_to_list_variable():
    assert (
        helper("add_item_to_list_variable", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('A')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4}"""
    )


# - Delete item in list
def test_ast_delete_item_in_list_base():
    assert (
        helper("delete_item_in_list_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="DeleteItemInListNode(variable:'my_list')"]
6 [label="NumericalNode(2.0)"]
7 [label="WriteNode"]
8 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8}"""
    )


def test_ast_delete_item_in_list_variable():
    assert (
        helper("delete_item_in_list_variable", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(1.0)"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="DeleteItemInListNode(variable:'my_list')"]
8 [label="VariableNode(name:'my_variable')"]
9 [label="WriteNode"]
10 [label="VariableNode(name:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9
9 -> 10}"""
    )


# - Delete all items in list
def test_ast_delete_all_items_in_list():
    assert (
        helper("delete_all_items_in_list", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="DeleteAllItemsInListNode(variable:'my_list')"]
6 [label="WriteNode"]
7 [label="LengthOfListNode(variable:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7}"""
    )


# - Insert item at index
def test_ast_insert_item_at_index_base():
    assert (
        helper("insert_item_at_index_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="InsertItemAtIndexNode(variable:'my_list')"]
6 [label="LiteralNode('c')"]
7 [label="NumericalNode(1.0)"]
8 [label="WriteNode"]
9 [label="ItemAtIndexNode(variable:'my_list')"]
10 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
5 -> 8
8 -> 9
9 -> 10}"""
    )


def test_ast_insert_item_at_index_variable_index():
    assert (
        helper("insert_item_at_index_variable_index", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(2.0)"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="InsertItemAtIndexNode(variable:'my_list')"]
8 [label="LiteralNode('c')"]
9 [label="VariableNode(name:'my_variable')"]
10 [label="WriteNode"]
11 [label="ItemAtIndexNode(variable:'my_list')"]
12 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9
7 -> 10
10 -> 11
11 -> 12}"""
    )


def test_ast_insert_item_at_index_variable_item():
    assert (
        helper("insert_item_at_index_variable_item", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('c')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="InsertItemAtIndexNode(variable:'my_list')"]
8 [label="VariableNode(name:'my_variable')"]
9 [label="NumericalNode(1.0)"]
10 [label="WriteNode"]
11 [label="ItemAtIndexNode(variable:'my_list')"]
12 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9
7 -> 10
10 -> 11
11 -> 12}"""
    )


# - Replace item at index
def test_ast_replace_item_at_index_base():
    assert (
        helper("replace_item_at_index_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="ReplaceItemAtIndexNode(variable:'my_list')"]
4 [label="NumericalNode(1.0)"]
5 [label="LiteralNode('c')"]
6 [label="WriteNode"]
7 [label="ItemAtIndexNode(variable:'my_list')"]
8 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
3 -> 6
6 -> 7
7 -> 8}"""
    )


def test_ast_replace_item_at_index_variable_index():
    assert (
        helper("replace_item_at_index_variable_index", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(2.0)"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="ReplaceItemAtIndexNode(variable:'my_list')"]
8 [label="VariableNode(name:'my_variable')"]
9 [label="LiteralNode('c')"]
10 [label="WriteNode"]
11 [label="ItemAtIndexNode(variable:'my_list')"]
12 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
7 -> 9
7 -> 10
10 -> 11
11 -> 12}"""
    )


def test_ast_replace_item_at_index_variable_value():
    assert (
        helper("replace_item_at_index_variable_value", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('c')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="ReplaceItemAtIndexNode(variable:'my_list')"]
6 [label="NumericalNode(1.0)"]
7 [label="VariableNode(name:'my_variable')"]
8 [label="WriteNode"]
9 [label="ItemAtIndexNode(variable:'my_list')"]
10 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
5 -> 8
8 -> 9
9 -> 10}"""
    )


# - Item at Index
def test_ast_item_at_index_base():
    assert (
        helper("item_at_index_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="WriteNode"]
6 [label="ItemAtIndexNode(variable:'my_list')"]
7 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7}"""
    )


def test_ast_item_at_index_variable():
    assert (
        helper("item_at_index_variable", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="NumericalNode(1.0)"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="WriteNode"]
8 [label="ItemAtIndexNode(variable:'my_list')"]
9 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
8 -> 9}"""
    )


# - Index of item
def test_ast_index_of_item_base():
    assert (
        helper("index_of_item_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="WriteNode"]
6 [label="IndexOfItemNode(variable:'my_list')"]
7 [label="LiteralNode('b')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7}"""
    )


def test_ast_index_of_item_variable():
    assert (
        helper("index_of_item_variable", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('a')"]
5 [label="AddItemToListNode(variable:'my_list')"]
6 [label="LiteralNode('b')"]
7 [label="WriteNode"]
8 [label="IndexOfItemNode(variable:'my_list')"]
9 [label="VariableNode(name:'my_variable')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
5 -> 7
7 -> 8
8 -> 9}"""
    )


# - Length of list
def test_ast_length_of_list():
    assert (
        helper("length_of_list", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="WriteNode"]
6 [label="LengthOfListNode(variable:'my_list')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6}"""
    )


# - List contains
def test_ast_list_contains_base():
    assert (
        helper("list_contains_base", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="AddItemToListNode(variable:'my_list')"]
2 [label="LiteralNode('a')"]
3 [label="IfThenNode"]
4 [label="ListContainsNode(variable:'my_list')"]
5 [label="LiteralNode('a')"]
6 [label="WriteNode"]
7 [label="LiteralNode('a')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
4 -> 5
3 -> 6
6 -> 7}"""
    )


def test_ast_list_contains_variable():
    assert (
        helper("list_contains_variable", "Variables")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="SetVariableToNode(variable:'my_variable')"]
2 [label="LiteralNode('a')"]
3 [label="AddItemToListNode(variable:'my_list')"]
4 [label="LiteralNode('b')"]
5 [label="IfThenNode"]
6 [label="ListContainsNode(variable:'my_list')"]
7 [label="VariableNode(name:'my_variable')"]
8 [label="WriteNode"]
9 [label="LiteralNode('a')"]
0 -> 1
1 -> 2
1 -> 3
3 -> 4
3 -> 5
5 -> 6
6 -> 7
5 -> 8
8 -> 9}"""
    )
