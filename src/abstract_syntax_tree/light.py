from enum import Enum

from src.abstract_syntax_tree import Node, StackNode, UIDGenerator


class TurnOnForDurationNode(StackNode):
    """Class to represent the TurnOnForDuration block."""

    def __init__(self, image, duration: Node, next: Node) -> None:
        super().__init__(next)
        self.image = image
        self.duration = duration

    def __str__(self) -> str:
        return f"TurnOnForDurationNode(image: '{self.image}')"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.duration.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class TurnOnNode(StackNode):
    """Class to represent the TurnOnForDuration block."""

    def __init__(self, image, next: Node) -> None:
        super().__init__(next)
        self.image = image

    def __str__(self) -> str:
        return f"TurnOnNode(image: '{self.image}')"


class WriteNode(StackNode):
    """Class to represent the WriteNode block."""

    def __init__(self, text: Node, next: Node) -> None:
        super().__init__(next)
        self.text = text

    def __str__(self) -> str:
        return "WriteNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.text.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class TurnOffPixelsNode(StackNode):
    """Class to represent the TurnOffPixels block."""

    def __init__(self, next: Node) -> None:
        super().__init__(next)

    def __str__(self) -> str:
        return "TurnOffPixelsNode"


class SetPixelBrightnessNode(StackNode):
    """Class to represent the SetPixelBrightness block."""

    def __init__(self, brightness: Node, next: Node) -> None:
        super().__init__(next)
        self.brightness = brightness

    def __str__(self) -> str:
        return "SetPixelBrightnessNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.brightness.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class SetPixelNode(StackNode):
    """Class to represent the SetPixel block."""

    def __init__(self, x: Node, y: Node, brightness: Node, next: Node) -> None:
        super().__init__(next)
        self.x = x
        self.y = y
        self.brightness = brightness

    def __str__(self) -> str:
        return "SetPixelNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.x.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
        self.y.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
        self.brightness.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class CenterButtonColor(Enum):
    """Enum for the color of the center button."""

    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    CYAN = "cyan"
    AZURE = "azure"
    PINK = "pink"
    WHITE = "white"
    BLACK = "black"

    def at(index: int) -> str:
        if index == 0:
            return CenterButtonColor.BLACK
        elif index == 1:
            return CenterButtonColor.PINK
        elif index == 3:
            return CenterButtonColor.AZURE
        elif index == 4:
            return CenterButtonColor.CYAN
        elif index == 5:
            return CenterButtonColor.GREEN
        elif index == 7:
            return CenterButtonColor.YELLOW
        elif index == 9:
            return CenterButtonColor.RED
        elif index == 10:
            return CenterButtonColor.WHITE
        else:
            raise ValueError(f"Invalid index {index}")

    def code(self) -> str:
        return self.value


class SetCenterButtonNode(StackNode):
    """Class to represent the SetCenterButton block."""

    def __init__(self, color: CenterButtonColor, next: Node) -> None:
        super().__init__(next)
        self.color = color

    def __str__(self) -> str:
        return f"SetCenterButtonNode(color: '{self.color}')"


class LightUpDistanceSensorNode(StackNode):
    """Class to represent the LightUpDistanceSensor block."""

    def __init__(self, port: Node, pattern, next: Node) -> None:
        super().__init__(next)
        self.port = port
        self.pattern = pattern

    def __str__(self) -> str:
        return f"LightUpDistanceSensorNode(pattern: '{self.pattern}')"

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
