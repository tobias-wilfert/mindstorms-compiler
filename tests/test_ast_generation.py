# Test to check that the AST is generated correctly.

from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


def ast_helper(filename: str, directory: str = ".") -> str:
    """Helper function that contains thee logic to test if the ast for a certain file is generated corrertly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    :return: String representation of the AST.
    :rtype: str
    """
    concrete_syntax_tree = filter_json(
        extract_json(f"tests/inputs/{directory}/{filename}/{filename}.lms")
    )
    visitor = Visitor()
    abstract_sytnax_tree = visitor.visit(concrete_syntax_tree)
    return abstract_sytnax_tree.tree_representation()


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
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_counterclockwise():
    assert (
        ast_helper("run_motor_for_duration_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.COUNTERCLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_degrees():
    assert (
        ast_helper("run_motor_for_duration_degrees", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.DEGREES',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_multiple_motors():
    assert (
        ast_helper("run_motor_for_duration_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A', 'E']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_multiple_motors3():
    assert (
        ast_helper("run_motor_for_duration_multiple_motors3", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A', 'B', 'C']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_all_motors():
    assert (
        ast_helper("run_motor_for_duration_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A', 'B', 'C', 'D', 'E', 'F']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_seconds():
    assert (
        ast_helper("run_motor_for_duration_seconds", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.SECONDS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_value_node():
    assert (
        ast_helper("run_motor_for_duration_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.PLUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# - Motor Go to Position
def test_ast_motor_go_to_position_base():
    assert (
        ast_helper("motor_go_to_position_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(ports:'['A']', direction:'GoDirection.SHORTEST')"]
2 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_motor_go_to_position_clockwise():
    assert (
        ast_helper("motor_go_to_position_clockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(ports:'['A']', direction:'GoDirection.CLOCKWISE')"]
2 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_motor_go_to_position_counterclockwise():
    assert (
        ast_helper("motor_go_to_position_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(ports:'['A']', direction:'GoDirection.COUNTERCLOCKWISE')"]
2 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_motor_go_to_position_multiple_motors():
    assert (
        ast_helper("motor_go_to_position_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(ports:'['A', 'B']', direction:'GoDirection.SHORTEST')"]
2 [label="NumericalNode(0.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_motor_go_to_position_value_node():
    assert (
        ast_helper("motor_go_to_position_value_node", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="MotorGoToPositionNode(ports:'['A']', direction:'GoDirection.SHORTEST')"]
2 [label="ArithmaticalNode(op:'Operation.PLUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


# - Start Motor
def test_ast_start_motor_base():
    assert (
        ast_helper("start_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE')"]
0 -> 1}"""
    )


def test_ast_start_motor_all_motors():
    assert (
        ast_helper("start_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(ports:'['A', 'B', 'C', 'D', 'E', 'F']', direction:'TurnDirection.CLOCKWISE')"]
0 -> 1}"""
    )


def test_ast_start_motor_multiple_motors():
    assert (
        ast_helper("start_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(ports:'['A', 'B']', direction:'TurnDirection.CLOCKWISE')"]
0 -> 1}"""
    )


def test_ast_start_motor_counterclockwise():
    assert (
        ast_helper("start_motor_counterclockwise", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StartMotorNode(ports:'['A']', direction:'TurnDirection.COUNTERCLOCKWISE')"]
0 -> 1}"""
    )


# - Stop Motor
def test_ast_stop_motor_base():
    assert (
        ast_helper("stop_motor_base", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode(ports:'['A']')"]
0 -> 1}"""
    )


def test_ast_stop_motor_all_motors():
    assert (
        ast_helper("stop_motor_all_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode(ports:'['A', 'B', 'C', 'D', 'E', 'F']')"]
0 -> 1}"""
    )


def test_ast_stop_motor_multiple_motors():
    assert (
        ast_helper("stop_motor_multiple_motors", "Motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="StopMotorNode(ports:'['A', 'B']')"]
0 -> 1}"""
    )


# ---------- Operators ----------
def test_ast_arithmatic():
    assert (
        ast_helper("arithmatic", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.PLUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="ArithmaticalNode(op:'Operation.MINUS')"]
5 [label="NumericalNode(2.0)"]
6 [label="ArithmaticalNode(op:'Operation.MULTIPLY')"]
7 [label="NumericalNode(3.0)"]
8 [label="ArithmaticalNode(op:'Operation.DIVIDE')"]
9 [label="NumericalNode(4.0)"]
10 [label="NumericalNode(5.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4
4 -> 5
4 -> 6
6 -> 7
6 -> 8
8 -> 9
8 -> 10}"""
    )


def test_ast_divide():
    assert (
        ast_helper("divide", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.DIVIDE')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_minus():
    assert (
        ast_helper("minus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.MINUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_multiply():
    assert (
        ast_helper("multiply", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.MULTIPLY')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )


def test_ast_plus():
    assert (
        ast_helper("plus", "Operators")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'TurnDirection.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="ArithmaticalNode(op:'Operation.PLUS')"]
3 [label="NumericalNode(1.0)"]
4 [label="NumericalNode(2.0)"]
0 -> 1
1 -> 2
2 -> 3
2 -> 4}"""
    )
