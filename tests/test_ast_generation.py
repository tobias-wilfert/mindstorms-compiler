# Test to check that the AST is generated correctly.

from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


def ast_helper(filename: str) -> str:
    """Helper function that contains thee logic to test if the ast for a certain file is generated corrertly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    :return: String representation of the AST.
    :rtype: str
    """
    concrete_syntax_tree = filter_json(
        extract_json(f"tests/inputs/{filename}/{filename}.lms")
    )
    visitor = Visitor()
    abstract_sytnax_tree = visitor.visit(concrete_syntax_tree)
    return abstract_sytnax_tree.tree_representation()


def test_ast_empty():
    assert ast_helper("run_motor_for_duration_base")


def test_ast_run_motor_for_duration_base():
    assert (
        ast_helper("run_motor_for_duration_base")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'Direction.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_counterclockwise():
    assert (
        ast_helper("run_motor_for_duration_counterclockwise")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'Direction.COUNTERCLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_degrees():
    assert (
        ast_helper("run_motor_for_duration_degrees")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'Direction.CLOCKWISE', unit:'Unit.DEGREES',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_multiple_motors():
    assert (
        ast_helper("run_motor_for_duration_multiple_motors")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A', 'E']', direction:'Direction.CLOCKWISE', unit:'Unit.ROTATIONS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_ast_run_motor_for_duration_seconds():
    assert (
        ast_helper("run_motor_for_duration_seconds")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
1 [label="RunMotorForDurationNode(ports:'['A']', direction:'Direction.CLOCKWISE', unit:'Unit.SECONDS',)"]
2 [label="NumericalNode(1.0)"]
0 -> 1
1 -> 2}"""
    )


def test_extract_json_when_program_starts():
    assert (
        ast_helper("when_program_starts")
        == """digraph {rankdir="TB"
0 [label="WhenProgramStartsNode"]
}"""
    )
