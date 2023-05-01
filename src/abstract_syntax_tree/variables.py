from src.abstract_syntax_tree import BooleanNode, Node, StackNode, UIDGenerator


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


class DeleteItemInListNode(StackNode):
    """Class to represent Delete Item in List block."""

    def __init__(self, list: str, index: Node, next: Node) -> None:
        super().__init__(next)
        self.list = list
        self.index = index

    def __str__(self) -> str:
        return f"DeleteItemInListNode(variable:'{self.list}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.index.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class DeleteAllItemsInListNode(StackNode):
    """Class to represent Delete all items in list block."""

    def __init__(self, list: str, next: Node) -> None:
        super().__init__(next)
        self.list = list

    def __str__(self) -> str:
        return f"DeleteAllItemsInListNode(variable:'{self.list}')"


class LengthOfListNode(Node):
    """Class to represent the Length of List block."""

    def __init__(self, variable) -> None:
        super().__init__()
        self.variable = variable

    def __str__(self) -> str:
        return f"LengthOfListNode(variable:'{self.variable}')"


class InsertItemAtIndexNode(StackNode):
    """Class to represent the Insert Item at Index block."""

    def __init__(self, variable: str, value: Node, index: Node, next: Node) -> None:
        super().__init__(next)
        self.variable = variable
        self.value = value
        self.index = index

    def __str__(self) -> str:
        return f"InsertItemAtIndexNode(variable:'{self.variable}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the value
        self.value.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )

        # Generate the representation of the index
        self.index.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ItemAtIndexNode(Node):
    """Class to represent the Item at Index block."""

    def __init__(self, variable, index) -> None:
        super().__init__()
        self.variable = variable
        self.index = index

    def __str__(self) -> str:
        return f"ItemAtIndexNode(variable:'{self.variable}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the index
        self.index.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ReplaceItemAtIndexNode(StackNode):
    """Class to represent the Replace Item at Index block."""

    def __init__(self, variable, index, value, next) -> None:
        super().__init__(next)
        self.variable = variable
        self.index = index
        self.value = value

    def __str__(self) -> str:
        return f"ReplaceItemAtIndexNode(variable:'{self.variable}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the index
        self.index.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )

        # Generate the representation of the value
        self.value.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class IndexOfItemNode(Node):
    """Class to represent the Index of Item block."""

    def __init__(self, variable: str, value: Node) -> None:
        super().__init__()
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f"IndexOfItemNode(variable:'{self.variable}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the value
        self.value.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ListContainsNode(BooleanNode):
    """Class to represent the ListContainsItem block."""

    def __init__(self, variable: str, value: Node) -> None:
        super().__init__()
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f"ListContainsNode(variable:'{self.variable}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the value
        self.value.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
