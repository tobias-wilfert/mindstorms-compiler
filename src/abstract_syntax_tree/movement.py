from src.abstract_syntax_tree import Node, StackNode, UIDGenerator


class SetMovementMotorsNode(StackNode):
    """Class to represent the SetMovementMotors block."""

    def __init__(self, ports: Node, next: Node) -> None:
        super().__init__(next)
        self.ports = ports

    def __str__(self) -> str:
        return "SetMovementMotorsNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.ports.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
