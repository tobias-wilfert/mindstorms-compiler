from enum import Enum

from src.abstract_syntax_tree import BooleanNode, Node, StackNode


class HubInteraction(Enum):
    SHAKE = "shaken"
    TAPPED = "tapped"
    FREEFALL = "falling"

    def code(self) -> str:
        return self.value


class HubInteractionNode(BooleanNode):
    """Class to represent the HubInteraction block."""

    def __init__(self, interaction: HubInteraction) -> None:
        super().__init__()
        self.interaction = interaction

    def __str__(self) -> str:
        return f"HubInteractionNode(interaction: '{self.interaction}')"


class SensorColor(Enum):
    BLACK = "'black'"
    VIOLET = "'violet'"
    BLUE = "'blue'"
    CYAN = "'cyan'"
    GREEN = "'green'"
    YELLOW = "'yellow'"
    RED = "'red'"
    WHITE = "'white'"
    NONE = None

    def at(index: int):
        if index == 0:
            return SensorColor.BLACK
        elif index == 1:
            return SensorColor.VIOLET
        elif index == 3:
            return SensorColor.BLUE
        elif index == 4:
            return SensorColor.CYAN
        elif index == 5:
            return SensorColor.GREEN
        elif index == 7:
            return SensorColor.YELLOW
        elif index == 9:
            return SensorColor.RED
        elif index == 10:
            return SensorColor.WHITE
        elif index == -1:
            return SensorColor.NONE
        else:
            raise ValueError(f"Invalid color index: {index}")

    def code(self) -> str:
        return self.value


class IsColorNode(BooleanNode):
    """Class to represent the IsColor block."""

    def __init__(self, port: Node, color: SensorColor) -> None:
        super().__init__()
        self.port = port
        self.color = color

    def __str__(self) -> str:
        return f"IsColorNode(color: '{self.color}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ColorNode(Node):
    """Class to represent the Color block."""

    def __init__(self, port: Node) -> None:
        super().__init__()
        self.port = port

    def __str__(self) -> str:
        return "ColorNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ReflectionComparator(Enum):
    LESS = "<"
    EQUAL = "=="
    GREATER = ">"

    def code(self) -> str:
        return self.value

    def parse(string):
        if string == "<":
            return ReflectionComparator.LESS
        elif string == "=":
            return ReflectionComparator.EQUAL
        elif string == ">":
            return ReflectionComparator.GREATER
        else:
            raise ValueError(f"Invalid reflection comparator: {string}")


class IsReflectionNode(BooleanNode):
    """Class to represent the IsReflection block."""

    def __init__(
        self, port: Node, comparator: ReflectionComparator, reflection: int
    ) -> None:
        super().__init__()
        self.port = port
        self.comparator = comparator
        self.reflection = reflection

    def __str__(self) -> str:
        return f"IsReflectionNode(reflection: '{self.comparator}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )

        self.reflection.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class ReflectedLightNode(Node):
    """Class to represent the ReflectedLight block."""

    def __init__(self, port: Node) -> None:
        super().__init__()
        self.port = port

    def __str__(self) -> str:
        return "ReflectedLightNode"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class DistanceComparator(Enum):
    LESS = "<"
    EQUAL = "=="
    GREATER = ">"

    def code(self) -> str:
        return self.value

    def parse(string):
        if string == "<":
            return DistanceComparator.LESS
        elif string == "=":
            return DistanceComparator.EQUAL
        elif string == ">":
            return DistanceComparator.GREATER
        else:
            raise ValueError(f"Invalid distance comparator: {string}")


class DistanceUnit(Enum):
    CM = "cm"
    INCHES = "inches"
    PERCENT = "percentage"

    def code(self) -> str:
        return self.value

    def parse(string):
        if string == "cm":
            return DistanceUnit.CM
        elif string == "inches":
            return DistanceUnit.INCHES
        elif string == "%":
            return DistanceUnit.PERCENT
        else:
            raise ValueError(f"Invalid distance unit: {string}")


class IsDistanceNode(BooleanNode):
    """Class to represent the IsDistance block."""

    def __init__(
        self,
        port: Node,
        comparator: ReflectionComparator,
        distance: int,
        unit: DistanceUnit,
    ) -> None:
        super().__init__()
        self.port = port
        self.comparator = comparator
        self.distance = distance
        self.unit = unit

    def __str__(self) -> str:
        return f"IsDistanceNode(distance: '{self.comparator}', unit: '{self.unit}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )

        self.distance.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class DistanceNode(Node):
    """Class to represent the Distance block."""

    def __init__(self, port: Node, unit: DistanceUnit) -> None:
        super().__init__()
        self.port = port
        self.unit = unit

    def __str__(self) -> str:
        return f"DistanceNode(unit: '{self.unit}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.port.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class GestureNode(Node):
    """Class to represent the Gesture block."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "GestureNode"


class HubOrientation(Enum):
    FRONT = "front"
    BACK = "back"
    UP = "up"
    DOWN = "down"
    LEFTSIDE = "leftside"
    RIGHTSIDE = "rightside"


class IsOrientationNode(BooleanNode):
    """Class to represent the IsOrientation block."""

    def __init__(self, orientation: HubOrientation) -> None:
        super().__init__()
        self.orientation = orientation

    def __str__(self) -> str:
        return f"IsOrientationNode(orientation: '{self.orientation}')"


class OrientationNode(Node):
    """Class to represent the Orientation block."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "OrientationNode"


class SetYawAngleNode(StackNode):
    """Class to represent the SetYawAngle block."""

    def __init__(self, next_node) -> None:
        super().__init__(next_node)

    def __str__(self) -> str:
        return "SetYawAngleNode"


class ButtonType(Enum):
    LEFT = "left"
    RIGHT = "right"


class ButtonAction(Enum):
    PRESSED = "pressed"
    RELEASED = "released"


class IsButtonPressedNode(BooleanNode):
    """Class to represent the IsButtonPressed block."""

    def __init__(self, button: ButtonType, action: ButtonAction) -> None:
        super().__init__()
        self.button = button
        self.action = action

    def __str__(self) -> str:
        return f"IsButtonPressedNode(button: '{self.button}', action: '{self.action}')"


class AngleUnit(Enum):
    PITCH = "pitch"
    ROLL = "roll"
    YAW = "yaw"


class HubAngleNode(Node):
    """Class to represent the HubAngle block."""

    def __init__(self, unit: AngleUnit) -> None:
        super().__init__()
        self.unit = unit

    def __str__(self) -> str:
        return f"HubAngleNode(unit: '{self.unit}')"


class TimerNode(Node):
    """Class to represent the Timer block."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "TimerNode"


class ResetTimerNode(StackNode):
    """Class to represent the ResetTimer block."""

    def __init__(self, next_node) -> None:
        super().__init__(next_node)

    def __str__(self) -> str:
        return "ResetTimerNode"


class IsKeyPressedNode(BooleanNode):
    """Class to represent the IsKeyPressed block."""

    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key

    def __str__(self) -> str:
        return f"IsKeyPressedNode(key: '{self.key}')"
