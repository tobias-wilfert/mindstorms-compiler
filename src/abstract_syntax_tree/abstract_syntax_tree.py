from enum import Enum


class UIDGenerator:
    """Simple UID generator."""

    def __init__(self) -> None:
        self.count = -1

    def get_uid(self) -> int:
        self.count += 1
        return self.count


class AST:
    """Abstract Syntax Tree that holds a list of hat nodes, which each represent a code stack."""

    # List of hat nodes, each can be interpreted as a sub tree, as such this is a forrest.
    # Needed since multiple code stacks can be present in a progam (i.e, function declarations)
    hat_nodes: list

    def __init__(self) -> None:
        self.hat_nodes = []

    def tree_representation(self, file_name: str = None) -> str:
        """Generates a dot representation of the AST and writes it to a file is file_name is provided.

        :param file_name: The name of the file to write the representation to, defaults to None.
        :type file_name: str, optional
        :return: The dot source code, or a string specifying where the code is written to.
        :rtype: str
        """
        nodes = []
        connections = []
        uid_generator = UIDGenerator()
        for hat_root in self.hat_nodes:
            hat_root.genereate_tree_representation(
                nodes, connections, -1, uid_generator
            )

        full_representation = (
            'digraph {rankdir="TB"\n'
            + "\n".join(nodes)
            + "\n"
            + "\n".join(connections)
            + "}"
        )

        if file_name:
            with open(file_name + ".gv", "a") as file:
                file += full_representation
            return f"The representaion is written to {file_name}.gv"
        else:
            return full_representation


class Node:
    """Base class for all the nodes that can be found in the AST."""

    def __init__(self) -> None:
        pass

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        """Generates the representation for this node

        :param nodes: Declerations of all the nodes.
        :type nodes: list
        :param connections: Connections between the nodes.
        :type connections: list
        :param parent_id: The id of the parent node.
        :type parent_id: int
        :param uid_generator: UID-generator so that every node can generates its own uid.
        :type uid_generator: UIDGenerator
        """
        raise NotImplementedError(
            "genereate_tree_representation() was called in the base class."
        )


class StackNode(Node):
    """The Base class for all Stack block, that are blocks which have a next pointer."""

    def __init__(self, next) -> None:
        super().__init__()
        self.next = next


class WhenProgramStartsNode(StackNode):
    """Class to represent the WhenProgramStarts block.
    Keeps track of the x and y position of the block for later code generation."""

    def __init__(self, x: int, y: int, next: Node) -> None:
        super().__init__(next)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "WhenProgramStartsNode"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        # Claim a node_id and update the node_counter
        node_id = uid_generator.get_uid()
        # Add the node representation to nodes, based on __str__
        nodes.append(f'{node_id} [label="{self}"]')
        # Generate the representation of the next node if there is one
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class Operation(Enum):
    PLUS = 1
    MINUS = 2
    DIVIDE = 3
    MULTIPLY = 4


class ArithmaticalNode(Node):
    def __init__(self, operation: Operation, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.op = operation
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return f"ArithmaticalNode(op:'{self.op}')"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')
        self.left_hand.genereate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.genereate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class NumericalNode(Node):
    """Class to represent any numerical value, float or int."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # Could be both Float or Int

    def __str__(self) -> str:
        return f"NumericalNode({self.value})"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')


class TurnDirection(Enum):
    """Enum for the directions that can be used in the RunMotor blocks."""

    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


class Unit(Enum):
    """Enum for the units that can be used in the RunMotor blocks."""

    ROTATIONS = 1
    SECONDS = 2
    DEGREES = 3


class RunMotorForDurationNode(StackNode):
    """Class to represent RunMotorForDuration blocks."""

    def __init__(
        self, ports: list, direction: TurnDirection, value: Node, unit: Unit, next: Node
    ) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"RunMotorForDurationNode(ports:'{self.ports}', direction:'{self.direction}', unit:'{self.unit}',)"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')
        self.value.genereate_tree_representation(
            nodes, connections, node_id, uid_generator
        )

        # If there is a connection add it and epxlore further into the tree
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class GoDirection(Enum):
    """Enum for the directions that can be used in the MotorGoToPosition blocks."""

    SHORTEST = 1
    CLOCKWISE = 2
    COUNTERCLOCKWISE = 3


class MotorGoToPositionNode(StackNode):
    """Class to represent MotorGoToPosition block."""

    def __init__(
        self, ports: list, direction: GoDirection, value: Node, next: Node
    ) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction
        self.value = value

    def __str__(self) -> str:
        return (
            f"MotorGoToPositionNode(ports:'{self.ports}', direction:'{self.direction}')"
        )

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')

        self.value.genereate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        # If there is a connection add it and epxlore further into the tree
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class StartMotorNode(StackNode):
    """Class to represent StartMotor block."""

    def __init__(self, ports: list, direction: TurnDirection, next: Node) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction

    def __str__(self) -> str:
        return f"StartMotorNode(ports:'{self.ports}', direction:'{self.direction}')"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')

        # If there is a connection add it and epxlore further into the tree
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class StopMotorNode(StackNode):
    """Class to represent StopMotor block."""

    def __init__(self, ports: list, next: Node) -> None:
        super().__init__(next)
        self.ports = ports

    def __str__(self) -> str:
        return f"StopMotorNode(ports:'{self.ports}')"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')

        # If there is a connection add it and epxlore further into the tree
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class SetMotorSpeedNode(StackNode):
    """Class to represent SetMotorSpeed block."""

    def __init__(self, ports: list, value: Node, next: Node) -> None:
        super().__init__(next)
        self.ports = ports
        self.value = value

    def __str__(self) -> str:
        return f"SetMotorSpeedNode(ports:'{self.ports}')"

    def genereate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        node_id = uid_generator.get_uid()

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')

        self.value.genereate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        # If there is a connection add it and epxlore further into the tree
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, uid_generator
            )
