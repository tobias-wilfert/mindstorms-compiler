from src.abstract_syntax_tree import Node, StackNode, UIDGenerator


class ListLiteralNode(Node):
    """Class to represent any list literal."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # List

    def __str__(self) -> str:
        return f"ListLiteralNode('{self.value}')"


class VariableNode(Node):
    """Class to represent the Variable and List block."""

    def __init__(self, name, id) -> None:
        super().__init__()
        self.name = name  # Variable name
        self.id = id  # The ID of the variable (unique, program wide)

    def __str__(self) -> str:
        return f"VariableNode(name:'{self.name}')"


class SetVariableToNode(StackNode):
    """Class to represent SetVariableTo block."""

    def __init__(self, variable: str, value: Node, next: Node) -> None:
        super().__init__(next)
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f"SetVariableToNode(variable:'{self.variable}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class ChangeVariableByNode(StackNode):
    """Class to represent ChangeVariableBy block."""

    def __init__(self, variable: str, value: Node, next: Node) -> None:
        super().__init__(next)
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f"ChangeVariableByNode(variable:'{self.variable}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class AddItemToListNode(StackNode):
    """Class to represent AddItemToList block."""

    def __init__(self, variable: str, value: Node, next: Node) -> None:
        super().__init__(next)
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f"AddItemToListNode(variable:'{self.variable}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
