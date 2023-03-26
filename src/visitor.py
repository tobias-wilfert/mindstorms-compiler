from src.abstract_syntax_tree.abstract_syntax_tree import (
    AST,
    ArithmeticalNode,
    ChangeVariableByNode,
    GoDirection,
    ListNode,
    LiteralNode,
    MotorGoToPositionNode,
    Node,
    NumericalNode,
    Operation,
    RunMotorForDurationNode,
    SetMotorSpeedNode,
    SetVariableToNode,
    StartMotorNode,
    StopMotorNode,
    TurnDirection,
    Unit,
    Variable,
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
        # TODO: This will need to be more sophisticated but this works for now
        if self.cst:
            return [next(iter(self.cst))]
        else:
            return []

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
        node = self.cst[
            node
        ]  # TODO: This can and will now break if the thing being references is a variable :/

        opcode = node["opcode"]
        if opcode == "flipperevents_whenProgramStarts":
            return self.visit_when_program_starts(node)
        elif opcode == "flippermotor_motorTurnForDirection":
            return self.visit_run_motor_for_duration(node)
        elif opcode == "flippermotor_motorGoDirectionToPosition":
            return self.visit_motor_go_to_position(node)
        elif opcode == "flippermotor_custom-angle":
            return self.visit_motor_custom_angle(node)
        elif opcode == "flippermotor_motorStartDirection":
            return self.visit_start_motor(node)
        elif opcode == "flippermotor_motorStop":
            return self.visit_stop_motor(node)
        elif opcode == "flippermotor_motorSetSpeed":
            return self.visit_set_motor_speed(node)
        elif opcode == "data_setvariableto":
            return self.visit_set_variable_to(node)
        elif opcode == "data_changevariableby":
            return self.visits_change_variable_by(node)
        elif opcode == "operator_add":
            return self.visit_operator(Operation.PLUS, node)
        elif opcode == "operator_subtract":
            return self.visit_operator(Operation.MINUS, node)
        elif opcode == "operator_divide":
            return self.visit_operator(Operation.DIVIDE, node)
        elif opcode == "operator_multiply":
            return self.visit_operator(Operation.MULTIPLY, node)
        else:
            raise NotImplementedError

    def visit_when_program_starts(self, node: dict) -> WhenProgramStartsNode:
        """Constructs the AST representation of the WhenProgramStarts node.
        :param node: The Node representation.
        """
        next_node = self.visit_node(node["next"])
        return WhenProgramStartsNode(node["x"], node["y"], next_node)

    def visit_run_motor_for_duration(self, node: dict) -> RunMotorForDurationNode:
        """Constructs the AST representation of the RunMotorForDuration node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_run_motor_for_duration_direction(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_run_motor_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return RunMotorForDurationNode(ports, direction, value, unit, next_node)

    def visit_run_motor_for_duration_port(self, node: dict) -> list:
        """Parses the ports that are being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: List of all the port names (single characters).
        """
        # If this is a list that the port is specified by a variable else by a list node
        port_specifier = node["inputs"]["PORT"][1]
        if isinstance(port_specifier, list):
            return Variable(port_specifier[1])
        else:
            ports = self.cst[port_specifier]["fields"][
                "field_flippermotor_multiple-port-selector"
            ][0]
            return ListNode(list(ports))

    def visit_run_motor_for_duration_direction(self, node: dict) -> TurnDirection:
        """Parses the direction that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = self.cst[node["inputs"]["DIRECTION"][1]]["fields"][
            "field_flippermotor_custom-icon-direction"
        ][0]
        return TurnDirection[direction.upper()]

    def visit_run_motor_for_duration_unit(self, node: dict) -> Unit:
        """Parses the unit that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The unit that is being used.
        """
        unit = node["fields"]["UNIT"][0]
        return Unit[unit.upper()]

    def visit_input(self, val) -> Node:
        """Visits the input field of a node.
        Val can be 2 things, if it is a list, than the 2 items is a string representation of a float or an int.
        If it is a string it is the identifier of a another node that needs to be parsed.

        :param val: Input representation.
        :type val: str or list
        :return: AST representation of the input.
        """
        if isinstance(val, list):
            try:
                return NumericalNode(float(val[1]))
            except ValueError:
                return LiteralNode(val[1])
        else:
            return self.visit_node(val)

    def visit_run_motor_for_duration_value(self, node: dict) -> Node:
        """Parses the value that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        # So while this is disgusting it seems to work :/
        # Would need to check if the length is 3
        if len(node["inputs"]["VALUE"][1]) == 3:
            return Variable(
                node["inputs"]["VALUE"][1][1]
            )  # TODO: Need to change this to also hold the id
        val = node["inputs"]["VALUE"][
            1
        ]  # TODO: This is also no longer working, which is a bit sad
        return self.visit_input(val)

    def visit_operator(self, op: Operation, node: dict) -> ArithmeticalNode:
        """Constructs the AST representation of the Arithmetics node.
        :param op: The operation of the arithmetic block
        :param node: The Node representation.
        :return: The AST representation.
        """
        left_hand = self.visit_input(node["inputs"]["NUM1"][1])
        right_hand = self.visit_input(node["inputs"]["NUM2"][1])
        return ArithmeticalNode(op, left_hand, right_hand)

    def visit_motor_go_to_position(self, node: dict) -> MotorGoToPositionNode:
        """Constructs the AST representation of the MotorGoToPosition node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_motor_go_to_position_direction(node)
        value = self.visit_motor_go_to_position_value(node)
        next_node = self.visit_node(node["next"])
        return MotorGoToPositionNode(ports, direction, value, next_node)

    def visit_motor_go_to_position_direction(self, node: dict) -> GoDirection:
        """Parse the direction used by the MotorGoToPositionNode.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = node["fields"]["DIRECTION"][0]
        return GoDirection[direction.upper()]

    def visit_motor_go_to_position_value(self, node: dict) -> Node:
        """Parse the value used by the MotorGoToPositionNode.
        :param node: The Node representation.
        :return: The value that is being used.
        """
        return self.visit_node(node["inputs"]["POSITION"][1])

    def visit_motor_custom_angle(self, node: dict) -> NumericalNode:
        """Parse the MotorCustomAngleNode.
        :param node: The Node representation.
        :return: The AST representation.
        """
        return NumericalNode(
            float(node["fields"]["field_flippermotor_custom-angle"][0])
        )

    def visit_start_motor(self, node: dict) -> StartMotorNode:
        """Constructs the AST representation of the StartMotor node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_run_motor_for_duration_direction(node)
        next_node = self.visit_node(node["next"])
        return StartMotorNode(ports, direction, next_node)

    def visit_stop_motor(self, node: dict) -> StopMotorNode:
        """Constructs the AST representation of the StopMotor node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return StopMotorNode(ports, next_node)

    def visit_set_motor_speed(self, node) -> SetMotorSpeedNode:
        """Constructs the AST representation of the SetMotorSpeed node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        value = self.visit_set_motor_speed_value(node)
        next_node = self.visit_node(node["next"])
        return SetMotorSpeedNode(ports, value, next_node)

    def visit_set_motor_speed_value(self, node: dict) -> Node:
        """Parse the value used by the SetMotorSpeedNode.
        :param node: The Node representation.
        :return: The value that is being used.
        """
        return self.visit_input(node["inputs"]["SPEED"][1])

    def visit_set_variable_to(self, node: dict) -> SetVariableToNode:
        """Constructs the AST representation of the SetVariableTo node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        # TODO: here we see that the id and the name of the variable is probably interesting to have
        #  This the  name of the variable, the id is at 1
        variable = node["fields"]["VARIABLE"][0]
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return SetVariableToNode(variable, value, next_node)

    def visits_change_variable_by(self, node) -> ChangeVariableByNode:
        """Constructs the AST representation of the ChangeVariable node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        variable = node["fields"]["VARIABLE"][
            0
        ]  # This the  name of the variable, the id is at 1
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return ChangeVariableByNode(variable, value, next_node)
