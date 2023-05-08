from enum import Enum

from src.abstract_syntax_tree import BooleanNode, Node


class Operation(Enum):
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"

    def code(self) -> str:
        return self.value


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


class PickRandomNumberNode(Node):
    def __init__(self, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "PickRandomNumberNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ComparisonOperator(Enum):
    EQUAL = "=="
    GREATER = ">"
    LESS = "<"
    AND = "and"
    OR = "or"
    IN = "in"

    def code(self) -> str:
        return self.value


class ComparisonNode(BooleanNode):
    def __init__(
        self, operation: ComparisonOperator, left_hand: Node, right_hand: Node
    ) -> None:
        super().__init__()
        self.op = operation
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return f"ComparisonNode(op:'{self.op}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class NotNode(BooleanNode):
    def __init__(self, left_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand

    def __str__(self) -> str:
        return "NotNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class IsBetweenNode(BooleanNode):
    def __init__(self, value: Node, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.value = value
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "IsBetweenNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.value.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class JoinStringsNode(Node):
    def __init__(self, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "JoinStringsNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class LetterOfStringNode(Node):
    def __init__(self, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "LetterOfStringNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class LengthOfStringNode(Node):
    def __init__(self, left_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand

    def __str__(self) -> str:
        return "LengthOfStringNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class StringContainsNode(BooleanNode):
    def __init__(self, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "StringContainsNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ModNode(Node):
    def __init__(self, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return "ModNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class RoundNode(Node):
    def __init__(self, left_hand: Node) -> None:
        super().__init__()
        self.left_hand = left_hand

    def __str__(self) -> str:
        return "RoundNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class UnaryFunction(Enum):
    TEN = "pow(10, "
    ABS = "abs("
    ACOS = "math.acos("
    ASIN = "math.asin("
    ATAN = "math.atan("
    CEIL = "math.ceil("
    COS = "math.cos("
    E = "pow(math.e, "
    FLOOR = "math.floor("
    LN = "math.log("
    LOG = "math.log2("
    SIN = "math.sin("
    SQRT = "math.sqrt("
    TAN = "math.tan("

    def code(self) -> str:
        return self.value

    def parse(function):
        if function == "10 ^":
            return UnaryFunction.TEN
        elif function == "abs":
            return UnaryFunction.ABS
        elif function == "acos":
            return UnaryFunction.ACOS
        elif function == "asin":
            return UnaryFunction.ASIN
        elif function == "atan":
            return UnaryFunction.ATAN
        elif function == "ceiling":
            return UnaryFunction.CEIL
        elif function == "cos":
            return UnaryFunction.COS
        elif function == "e ^":
            return UnaryFunction.E
        elif function == "floor":
            return UnaryFunction.FLOOR
        elif function == "ln":
            return UnaryFunction.LN
        elif function == "log":
            return UnaryFunction.LOG
        elif function == "sin":
            return UnaryFunction.SIN
        elif function == "sqrt":
            return UnaryFunction.SQRT
        elif function == "tan":
            return UnaryFunction.TAN
        else:
            raise ValueError(f"Invalid function {function}")


class UnaryMathFunctionNode(Node):
    def __init__(self, function: UnaryFunction, left_hand: Node) -> None:
        super().__init__()
        self.function = function
        self.left_hand = left_hand

    def __str__(self) -> str:
        return f"UnaryMathFunctionNode(function:'{self.function}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class BinaryFunction(Enum):
    ATAN2 = "math.atan2"
    COPYSIGN = "math.copysign"
    HYPOT = "math.hypot"
    MAX = "max"
    MIN = "min"
    POW = "pow"

    def code(self) -> str:
        return self.value

    def parse(function):
        if function == "atan2":
            return BinaryFunction.ATAN2
        elif function == "copysign":
            return BinaryFunction.COPYSIGN
        elif function == "hypot":
            return BinaryFunction.HYPOT
        elif function == "max":
            return BinaryFunction.MAX
        elif function == "min":
            return BinaryFunction.MIN
        elif function == "pow":
            return BinaryFunction.POW
        else:
            raise ValueError(f"Invalid function {function}")


class BinaryMathFunctionNode(Node):
    def __init__(
        self, function: BinaryFunction, left_hand: Node, right_hand: Node
    ) -> None:
        super().__init__()
        self.function = function
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return f"BinaryMathFunction(function:'{self.function}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
