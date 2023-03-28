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
    # Needed since multiple code stacks can be present in a program (i.e, function declarations)
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
            hat_root.generate_tree_representation(nodes, connections, -1, uid_generator)

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
            return f"The representation is written to {file_name}.gv"
        else:
            return full_representation


class Node:
    """Base class for all the nodes that can be found in the AST."""

    def __init__(self) -> None:
        pass

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Should be called if there is any custom representation logic that needs to be done
        pass

    def generate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        """Generates the representation for this node

        :param nodes: Decelerations of all the nodes.
        :type nodes: list
        :param connections: Connections between the nodes.
        :type connections: list
        :param parent_id: The id of the parent node.
        :type parent_id: int
        :param uid_generator: UID-generator so that every node can generates its own uid.
        :type uid_generator: UIDGenerator
        """
        # Claim a node_id and update the node_counter
        node_id = uid_generator.get_uid()
        # Add the node representation to nodes, based on __str__
        nodes.append(f'{node_id} [label="{self}"]')
        # Connect to parent, unless it is the first node
        if parent_id != -1:
            connections.append(f"{parent_id} -> {node_id}")
        # Do any custom logic if necessary
        self.custom_representation(nodes, connections, node_id, uid_generator)


class StackNode(Node):
    """The Base class for all Stack block, that are blocks which have a next pointer."""

    def __init__(self, next) -> None:
        super().__init__()
        self.next = next

    def generate_tree_representation(
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
        # Connect to parent, unless it is the first node
        if parent_id != -1:
            connections.append(f"{parent_id} -> {node_id}")
        # Do any custom logic if necessary
        self.custom_representation(nodes, connections, node_id, uid_generator)
        # If there is a next node also generate the representation for it
        if self.next:
            self.next.generate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class WhenProgramStartsNode(StackNode):
    """Class to represent the WhenProgramStarts block.
    Keeps track of the x and y position of the block for later code generation."""

    # TODO: This probably also needs to keep track of the variables that are being used in this stack

    def __init__(self, x: int, y: int, next: Node) -> None:
        super().__init__(next)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "WhenProgramStartsNode"


class Operation(Enum):
    PLUS = 1
    MINUS = 2
    DIVIDE = 3
    MULTIPLY = 4


class ArithmeticalNode(Node):
    def __init__(self, operation: Operation, left_hand: Node, right_hand: Node) -> None:
        super().__init__()
        self.op = operation
        self.left_hand = left_hand
        self.right_hand = right_hand

    def __str__(self) -> str:
        return f"ArithmeticalNode(op:'{self.op}')"

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Generate the representation of the left and right side
        self.left_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )
        self.right_hand.generate_tree_representation(
            nodes, connections, node_id, uid_generator
        )


class NumericalNode(Node):
    """Class to represent any numerical value, float or int."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # Could be both Float or Int

    def __str__(self) -> str:
        return f"NumericalNode({self.value})"


class LiteralNode(Node):
    """Class to represent any string literal."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # String

    def __str__(self) -> str:
        return f"LiteralNode('{self.value}')"


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
