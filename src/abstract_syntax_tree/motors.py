from enum import Enum

from src.abstract_syntax_tree import Node, StackNode, UIDGenerator


class TurnDirection(Enum):
    """Enum for the directions that can be used in the RunMotor blocks."""

    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


class Unit(Enum):
    """Enum for the units that can be used in the RunMotor blocks."""

    ROTATIONS = 1
    SECONDS = 2
    DEGREES = 3

    def code(self):
        if self == Unit.ROTATIONS:
            return "rotations"
        elif self == Unit.SECONDS:
            return "seconds"
        elif self == Unit.DEGREES:
            return "degrees"


class RunMotorForDurationNode(StackNode):
    """Class to represent RunMotorForDuration blocks."""

    def __init__(
        self, ports: Node, direction: TurnDirection, value: Node, unit: Unit, next: Node
    ) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return (
            f"RunMotorForDurationNode(direction:'{self.direction}', unit:'{self.unit}')"
        )

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
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class GoDirection(Enum):
    """Enum for the directions that can be used in the MotorGoToPosition blocks."""

    SHORTEST = 1
    CLOCKWISE = 2
    COUNTERCLOCKWISE = 3

    def code(self):
        if self == GoDirection.SHORTEST:
            return "shortest path"
        elif self == GoDirection.CLOCKWISE:
            return "clockwise"
        elif self == GoDirection.COUNTERCLOCKWISE:
            return "counterclockwise"


class MotorGoToPositionNode(StackNode):
    """Class to represent MotorGoToPosition block."""

    def __init__(
        self, ports: Node, direction: GoDirection, value: Node, next: Node
    ) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction
        self.value = value

    def __str__(self) -> str:
        return f"MotorGoToPositionNode(direction:'{self.direction}')"

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
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class StartMotorNode(StackNode):
    """Class to represent StartMotor block."""

    def __init__(self, ports: Node, direction: TurnDirection, next: Node) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction

    def __str__(self) -> str:
        return f"StartMotorNode(direction:'{self.direction}')"

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


class StopMotorNode(StackNode):
    """Class to represent StopMotor block."""

    def __init__(self, ports: Node, next: Node) -> None:
        super().__init__(next)
        self.ports = ports

    def __str__(self) -> str:
        return "StopMotorNode"

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


class SetMotorSpeedNode(StackNode):
    """Class to represent SetMotorSpeed block."""

    def __init__(self, ports: Node, value: Node, next: Node) -> None:
        super().__init__(next)
        self.ports = ports
        self.value = value

    def __str__(self) -> str:
        return "SetMotorSpeedNode"

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
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class MotorPositionNode(StackNode):
    """Class to represent MotorPosition block."""

    def __init__(self, port: Node, next: Node) -> None:
        super().__init__(next)
        self.port = port

    def __str__(self) -> str:
        return "MotorPositionNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.port.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class MotorSpeedNode(StackNode):
    """Class to represent MotorSpeed block."""

    def __init__(self, port: Node, next: Node) -> None:
        super().__init__(next)
        self.port = port

    def __str__(self) -> str:
        return "MotorSpeedNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.port.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
