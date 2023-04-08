from enum import Enum

from src.abstract_syntax_tree import Node


class Operation(Enum):
    PLUS = 1
    MINUS = 2
    DIVIDE = 3
    MULTIPLY = 4

    def code(self) -> str:
        if self == Operation.PLUS:
            return "+"
        elif self == Operation.MINUS:
            return "-"
        elif self == Operation.DIVIDE:
            return "/"
        elif self == Operation.MULTIPLY:
            return "*"


class ArithmeticalNode(Node):
    def __init__(self, operation: Operation, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.op = operation
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return f"ArithmeticalNode(op:'{self.op}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
