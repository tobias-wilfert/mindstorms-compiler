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
