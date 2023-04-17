from enum import Enum

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


class MovementUnit(Enum):
    """Enum for the units that can be used in the MoveForDuration block."""

    CM = "cm"
    INCHES = "in"
    ROTATIONS = "rotations"
    DEGREES = "degrees"
    SECONDS = "seconds"

    def code(self) -> str:
        return self.value


class MovementDirection(Enum):
    """Enum for the directions that can be used in the MoveForDuration block."""

    FORWARD = 0
    BACK = 1
    CLOCKWISE = 2
    COUNTERCLOCKWISE = 3


class MoveForDurationNode(StackNode):
    """Class to represent the MoveForDuration block."""

    def __init__(
        self, direction: MovementDirection, value: Node, unit: MovementUnit, next: Node
    ) -> None:
        super().__init__(next)
        self.direction = direction
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"MoveForDurationNode(direction:'{self.direction}', unit:'{self.unit}')"

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


class MoveWithSteeringNode(StackNode):
    """Class to represent the MoveWithSteeringNode block."""

    def __init__(
        self, steering: Node, value: Node, unit: MovementUnit, next: Node
    ) -> None:
        super().__init__(next)
        self.steering = steering
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"MoveWithSteeringNode(unit:'{self.unit}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.steering.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
        self.value.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class StartMovingWithSteering(StackNode):
    """Class to represent the MoveWithSteering block."""

    def __init__(self, steering: Node, next: Node) -> None:
        super().__init__(next)
        self.steering = steering

    def __str__(self) -> str:
        return "StartMowingWithSteeringNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.steering.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class StopMovingNode(StackNode):
    """Class to represent the StopMoving block."""

    def __init__(self, next: Node) -> None:
        super().__init__(next)

    def __str__(self) -> str:
        return "StopMovingNode"


class SetMovementSpeedNode(StackNode):
    """Class to represent the SetMovement block."""

    def __init__(self, value: Node, next: Node) -> None:
        super().__init__(next)
        self.value = value

    def __str__(self) -> str:
        return "SetMovementSpeedNode"

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


class RotationUnit(Enum):
    """Enum for the units that can be used in the SetMotorRotation block."""

    CM = "cm"
    INCHES = "in"

    def code(self):
        return self.value


class SetMotorRotationNode(StackNode):
    """Class to represent the SetMotorRotation block."""

    def __init__(self, value: Node, unit: MovementUnit, next: Node) -> None:
        super().__init__(next)
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"SetMotorRotationNode(unit:'{self.unit}')"

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
