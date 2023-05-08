from src.abstract_syntax_tree import BooleanNode, Node, StackNode, UIDGenerator


class IfThenNode(StackNode):
    """Class to represent If then block."""

    def __init__(self, condition: BooleanNode, body: Node, next: Node) -> None:
        super().__init__(next)
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return "IfThenNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.condition.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )

        self.body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class WaitForSecondsNode(StackNode):
    """Class to represent WaitForSeconds block."""

    def __init__(self, seconds: Node, next: Node) -> None:
        super().__init__(next)
        self.seconds = seconds

    def __str__(self) -> str:
        return "WaitForSecondsNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.seconds.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class WaitUntilNode(StackNode):
    """Class to represent WaitUntil block."""

    def __init__(self, condition: BooleanNode, next: Node) -> None:
        super().__init__(next)
        self.condition = condition

    def __str__(self) -> str:
        return "WaitUntilNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.condition.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class RepeatLoopNode(StackNode):
    """Class to represent Repeat Loop block."""

    def __init__(self, times: Node, body: Node, next: Node) -> None:
        super().__init__(next)
        self.times = times
        self.body = body

    def __str__(self) -> str:
        return "RepeatLoopNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.times.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )

        self.body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class ForeverLoopNode(StackNode):
    """Class to represent Forever Loop block."""

    def __init__(self, body: Node, next: Node) -> None:
        super().__init__(next)
        self.body = body

    def __str__(self) -> str:
        return "ForeverLoopNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class RepeatUntilNode(StackNode):
    """Class to represent Repeat Until block."""

    def __init__(self, condition: BooleanNode, body: Node, next: Node) -> None:
        super().__init__(next)
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return "RepeatUntilNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.condition.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )

        self.body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class IfElseNode(StackNode):
    """Class to represent If Else block."""

    def __init__(
        self, condition: BooleanNode, body: Node, else_body: Node, next: Node
    ) -> None:
        super().__init__(next)
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __str__(self) -> str:
        return "IfElseNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.condition.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )

        self.body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )

        self.else_body.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
