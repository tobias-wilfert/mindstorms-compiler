from src.abstract_syntax_tree import Node, StackNode, UIDGenerator


class PlaySoundUntilDoneNode(StackNode):
    """Class to represent the Play Sound until Done block."""

    def __init__(self, sound: str, next: Node) -> None:
        super().__init__(next)
        self.sound = sound

    def __str__(self):
        return f"PlaySoundUntilDoneNode(sound: '{self.sound}')"


class StartSoundNode(StackNode):
    """Class to represent the Start Sound block."""

    def __init__(self, sound: str, next: Node) -> None:
        super().__init__(next)
        self.sound = sound

    def __str__(self):
        return f"StartSoundNode(sound: '{self.sound}')"


class PlayBeepNode(StackNode):
    """Class to represent the Play Beep block."""

    def __init__(self, pitch: Node, duration: Node, next: Node) -> None:
        super().__init__(next)
        self.pitch = pitch
        self.duration = duration

    def __str__(self):
        return "PlayBeepNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.pitch.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )
        self.duration.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class StartBeepNode(StackNode):
    """Class to represent the Start Beep block."""

    def __init__(self, pitch: Node, next: Node) -> None:
        super().__init__(next)
        self.pitch = pitch

    def __str__(self):
        return "StartBeepNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.pitch.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class StopBeepNode(StackNode):
    """Class to represent the Stop Beep block."""

    def __init__(self, next: Node) -> None:
        super().__init__(next)

    def __str__(self):
        return "StopBeepNode"


class SetVolumeNode(StackNode):
    """Class to represent the Set Volume block."""

    def __init__(self, volume: Node, next: Node) -> None:
        super().__init__(next)
        self.volume = volume

    def __str__(self):
        return "SetVolumeNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.volume.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class ChangeVolumeNode(StackNode):
    """Class to represent the Change Volume block."""

    def __init__(self, volume: Node, next: Node) -> None:
        super().__init__(next)
        self.volume = volume

    def __str__(self):
        return "ChangeVolumeNode"

    def custom_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        self.volume.generate_tree_representation(
            nodes, connections, parent_id, uid_generator
        )


class VolumeNode(Node):
    """Class to represent the Volume block."""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "VolumeNode"
