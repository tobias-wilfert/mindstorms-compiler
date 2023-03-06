from src.abstract_syntax_tree.abstract_syntax_tree import (
    AST,
    Direction,
    Node,
    NumericalNode,
    RunMotorForDurationNode,
    Unit,
    WhenProgramStartsNode,
)


class Visitor:
    """This visits CST and generates the AST while doing so."""

    ast: AST  # The AST that is being constructed
    cst: dict

    def __init__(self) -> None:
        pass

    def visit(self, cst: dict) -> AST:
        # TODO: Need to do something with the variables, list, broadcast and extensions
        self.ast = AST()
        self.cst = cst["blocks"]

        # Parse all the subtrees that are present in the CST
        for node in self.find_root_nodes():
            self.ast.hat_nodes.append(self.visit_node(node))

        return self.ast

    def find_root_nodes(self) -> list:
        """Find all the root notes of the subtrees present in the CST. These are the first blocks of block stacks.
        :return: List of all the root nodes.
        :rtype: list
        """
        # TODO: This will need to be more suffisticated but this works for now
        return [next(iter(self.cst))]

    def visit_node(self, node: dict) -> Node:
        """Checks the type of the node and calls the appropriate visit function.
        :param node: The identifier of the current node (the key for the CST dict) or None
        :type node: dict
        :raises NotImplementedError: If the node is not yet supported raise an error
        :return: The AST representation of the node
        :rtype: Node
        """
        if not node:  # There is no node return None
            return None
        node = self.cst[node]

        opcode = node["opcode"]
        if opcode == "flipperevents_whenProgramStarts":
            return self.visit_when_program_starts(node)
        elif opcode == "flippermotor_motorTurnForDirection":
            return self.visit_run_motor_for_duration(node)
        else:
            raise NotImplementedError

    def visit_when_program_starts(self, node: dict) -> WhenProgramStartsNode:
        """Constructs the AST representation of the WhenProgramStarts node.
        :param node: The Node representation.
        :type node: dict
        :return: The AST representation.
        :rtype: WhenProgramStartsNode
        """
        next_node = self.visit_node(node["next"])
        return WhenProgramStartsNode(node["x"], node["y"], next_node)

    def visit_run_motor_for_duration(self, node: dict) -> RunMotorForDurationNode:
        """Constructs the AST representation of the RunMotorForDuration node.
        :param node: The Node representation.
        :type node: dict
        :return: The AST representation.
        :rtype: RunMotorForDurationNode
        """
        # TODO: Need test cases here for the case in which the value is a numerical block rather than just a value
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_run_motor_for_duration_direction(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_run_motor_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return RunMotorForDurationNode(ports, direction, value, unit, next_node)

    def visit_run_motor_for_duration_port(self, node: dict) -> list:
        """Parses the ports that are being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :type node: dict
        :return: List of all the port names (single characters).
        :rtype: list
        """
        ports = self.cst[node["inputs"]["PORT"][1]]["fields"][
            "field_flippermotor_multiple-port-selector"
        ][0]
        return list(ports)

    def visit_run_motor_for_duration_direction(self, node: dict) -> Direction:
        """Parses the direction that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :type node: dict
        :return: The direction that is being used.
        :rtype: Direction
        """
        direction = self.cst[node["inputs"]["DIRECTION"][1]]["fields"][
            "field_flippermotor_custom-icon-direction"
        ][0]
        return Direction[direction.upper()]

    def visit_run_motor_for_duration_unit(self, node: dict) -> Unit:
        """Parses the unit that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :type node: dict
        :return: The unit that is being used.
        :rtype: Unit
        """
        unit = node["fields"]["UNIT"][0]
        return Unit[unit.upper()]

    def visit_run_motor_for_duration_value(self, node) -> Node:
        """Parses the value that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :type node: dict
        :return: The node that that specifies the value that should be used. (Could be an entrie subtree, in the case of an equation).
        :rtype: Node
        """
        # Need to check if there are underlying nodes or if it is just a constant.
        val = node["inputs"]["VALUE"][1][1]

        # TODO: This entire check is very unelegant and as such it should be done differently because it is probably also dangerous
        try:
            return NumericalNode(float(val))
        except ValueError:
            return None  # TODO: Need to add the logic to explore the node here.
