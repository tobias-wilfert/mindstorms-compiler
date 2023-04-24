from src.abstract_syntax_tree import AST, CommentNode, LiteralNode, Node, NumericalNode
from src.abstract_syntax_tree.events import WhenProgramStartsNode
from src.abstract_syntax_tree.light import (
    CenterButtonColor,
    LightUpDistanceSensorNode,
    SetCenterButtonNode,
    SetPixelBrightnessNode,
    SetPixelNode,
    TurnOffPixelsNode,
    TurnOnForDurationNode,
    TurnOnNode,
    WriteNode,
)
from src.abstract_syntax_tree.motors import (
    GoDirection,
    MotorGoToPositionNode,
    MotorPositionNode,
    MotorSpeedNode,
    RunMotorForDurationNode,
    SetMotorSpeedNode,
    StartMotorNode,
    StopMotorNode,
    TurnDirection,
    Unit,
)
from src.abstract_syntax_tree.movement import (
    MoveForDurationNode,
    MovementDirection,
    MovementUnit,
    MoveWithSteeringNode,
    RotationUnit,
    SetMotorRotationNode,
    SetMovementMotorsNode,
    SetMovementSpeedNode,
    StartMovingWithSteering,
    StopMovingNode,
)
from src.abstract_syntax_tree.operators import ArithmeticalNode, Operation
from src.abstract_syntax_tree.variables import (
    AddItemToListNode,
    ChangeVariableByNode,
    ListLiteralNode,
    SetVariableToNode,
    VariableNode,
)


class Visitor:
    """This visits CST and generates the AST while doing so."""

    ast: AST  # The AST that is being constructed
    cst: dict

    best_effort: bool  # If true then the visitor will try to continue even if it encounters a block it can't translate.
    # A comment will be added to the AST to indicate that this has happened.

    def __init__(self, best_effort=True) -> None:
        self.best_effort = best_effort
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

    # flake8: noqa: C901
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
        elif opcode == "flippermotor_absolutePosition":
            return self.visit_motor_position(node)
        elif opcode == "flippermotor_speed":
            return self.visit_motor_speed(node)
        elif opcode == "flippermove_setMovementPair":
            return self.visit_set_movement_motors(node)
        elif opcode == "flippermove_move":
            return self.visit_move_for_duration(node)
        elif opcode == "flippermove_steer":
            return self.visit_move_with_steering(node)
        elif opcode == "flippermove_rotation-wheel":
            return self.visit_move_rotation_wheel(node)
        elif opcode == "flippermove_startSteer":
            return self.visit_start_moving_with_steering(node)
        elif opcode == "flippermove_stopMove":
            return self.visit_stop_moving(node)
        elif opcode == "flippermove_movementSpeed":
            return self.visit_set_movement_speed(node)
        elif opcode == "flippermove_setDistance":
            return self.visit_set_motor_rotation(node)
        elif opcode == "flipperdisplay_ledAnimation":
            return self.visit_start_animation(node)
        elif opcode == "flipperdisplay_ledAnimationUntilDone":
            return self.visit_play_animation_until_done(node)
        elif opcode == "flipperdisplay_ledImageFor":
            return self.visit_turn_on_for_duration(node)
        elif opcode == "flipperdisplay_ledImage":
            return self.visit_turn_on(node)
        elif opcode == "flipperdisplay_ledText":
            return self.visit_write(node)
        elif opcode == "flipperdisplay_displayOff":
            return self.visit_turn_off_pixels(node)
        elif opcode == "flipperdisplay_ledSetBrightness":
            return self.visit_set_pixel_brightness(node)
        elif opcode == "flipperdisplay_ledOn":
            return self.visit_set_pixel(node)
        elif opcode == "flipperdisplay_menu_ledMatrixIndex":
            return self.visit_set_pixel_matrix_index(node)
        elif opcode == "flipperdisplay_ledRotateDirection":
            return self.visit_rotate_orientation(node)
        elif opcode == "flipperdisplay_ledRotateOrientation":
            return self.visit_set_orientation(node)
        elif opcode == "flipperdisplay_centerButtonLight":
            return self.visit_set_center_button(node)
        elif opcode == "flipperdisplay_ultrasonicLightUp":
            return self.visit_light_up_distance_sensor(node)
        elif opcode == "data_setvariableto":
            return self.visit_set_variable_to(node)
        elif opcode == "data_changevariableby":
            return self.visits_change_variable_by(node)
        elif opcode == "data_addtolist":
            return self.visit_add_to_list(node)
        elif opcode == "operator_add":
            return self.visit_operator(Operation.PLUS, node)
        elif opcode == "operator_subtract":
            return self.visit_operator(Operation.MINUS, node)
        elif opcode == "operator_divide":
            return self.visit_operator(Operation.DIVIDE, node)
        elif opcode == "operator_multiply":
            return self.visit_operator(Operation.MULTIPLY, node)
        else:
            raise NotImplementedError(opcode)

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
        port_specifier = node["inputs"]["PORT"][1]
        if isinstance(port_specifier, list):
            return VariableNode(port_specifier[1], port_specifier[2])
        else:
            ports = self.cst[port_specifier]["fields"][
                "field_" + self.cst[port_specifier]["opcode"]
            ][0]
            return ListLiteralNode(list(ports))

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
        **NOTE**: If the list has 3 items it is actually a variable.
        If it is a string it is the identifier of a another node that needs to be parsed.

        :param val: Input representation.
        :type val: str or list
        :return: AST representation of the input.
        """
        if isinstance(val, list):
            if len(val) == 3:
                return VariableNode(val[1], val[2])
            else:
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
        return self.visit_input(node["inputs"]["VALUE"][1])

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
        if len(node["inputs"]["POSITION"][1]) == 3:
            return VariableNode(
                node["inputs"]["POSITION"][1][1], node["inputs"]["POSITION"][1][2]
            )
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
        # TODO: This needs to be fixed to also keep track of the variable ID and NAME
        variable = node["fields"]["VARIABLE"][0]
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return SetVariableToNode(variable, value, next_node)

    def visits_change_variable_by(self, node) -> ChangeVariableByNode:
        """Constructs the AST representation of the ChangeVariable node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        # TODO: This needs to be fixed to also keep track of the variable ID and NAME
        variable = node["fields"]["VARIABLE"][0]
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return ChangeVariableByNode(variable, value, next_node)

    def visit_add_to_list_value(self, node) -> Node:
        """Parses the value that is being used by the AddItemToList node.

        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        if len(node["inputs"]["ITEM"][1]) == 3:
            return VariableNode(
                node["inputs"]["ITEM"][1][1], node["inputs"]["ITEM"][1][2]
            )
        else:
            if isinstance(node["inputs"]["ITEM"][1], list):
                return LiteralNode(node["inputs"]["ITEM"][1][1])
            else:
                return self.visit_node(node["inputs"]["ITEM"][1])

    def visit_add_to_list(self, node) -> AddItemToListNode:
        """Constructs the AST representation of the AddItemToList node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        variable = node["fields"]["LIST"][0]
        value = self.visit_add_to_list_value(node)
        next_node = self.visit_node(node["next"])
        return AddItemToListNode(variable, value, next_node)

    def visit_motor_position(self, node) -> MotorPositionNode:
        """Constructs the AST representation of the MotorPosition node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return MotorPositionNode(port, next_node)

    def visit_motor_speed(self, node) -> MotorSpeedNode:
        """Constructs the AST representation of the MotorSpeed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return MotorSpeedNode(port, next_node)

    def visit_movement_ports(self, node: dict) -> Node:
        """Parses the ports that are being used by the SetMovementMotorsNode.
        :param node: The Node representation.
        :return: List of all the port names (single characters).
        """
        port_specifier = node["inputs"]["PAIR"][1]
        if isinstance(port_specifier, list):
            return VariableNode(port_specifier[1], port_specifier[2])
        else:
            ports = self.cst[port_specifier]["fields"][
                "field_" + self.cst[port_specifier]["opcode"]
            ][0]
            return ListLiteralNode(list(ports))

    def visit_set_movement_motors(self, node) -> SetMovementMotorsNode:
        """Constructs the AST representation of the SetMovementMotors node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_movement_ports(node)
        next_node = self.visit_node(node["next"])
        return SetMovementMotorsNode(ports, next_node)

    def visit_move_for_duration_unit(self, node: dict) -> MovementUnit:
        """Parses the unit that is being used by the MoveForDuration.
        :param node: The Node representation.
        :return: The unit that is being used.
        """
        unit = node["fields"]["UNIT"][0]
        return MovementUnit[unit.upper()]

    def visit_move_for_duration_direction(self, node: dict) -> MovementDirection:
        """Parses the direction that is being used by the MoveForDuration.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = self.cst[node["inputs"]["DIRECTION"][1]]["fields"][
            "field_flippermove_custom-icon-direction"
        ][0]
        return MovementDirection[direction.upper()]

    def visit_move_for_duration(self, node) -> MoveForDurationNode:
        """Constructs the AST representation of the MoveForDuration node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        direction = self.visit_move_for_duration_direction(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_move_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return MoveForDurationNode(direction, value, unit, next_node)

    def visit_move_with_steering_steering(self, node: dict) -> Node:
        """Parses the value that is being used by the MoveWithSteeringNode.
        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        return self.visit_input(node["inputs"]["STEERING"][1])

    def visit_move_rotation_wheel(self, node: dict) -> Node:
        """Parses the steering that is being used by the MoveWithSteeringNode.
        :param node: The Node representation.
        :return: A NumericalNode with the value of the steering.
        """
        return NumericalNode(
            float(node["fields"]["field_flippermove_rotation-wheel"][0])
        )

    def visit_move_with_steering(self, node) -> MoveWithSteeringNode:
        """Constructs the AST representation of the MoveWithSteering node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        steering = self.visit_move_with_steering_steering(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_move_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return MoveWithSteeringNode(steering, value, unit, next_node)

    def visit_start_moving_with_steering(self, node) -> StartMovingWithSteering:
        """Constructs the AST representation of the StartMovingWithSteering node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        steering = self.visit_move_with_steering_steering(node)
        next_node = self.visit_node(node["next"])
        return StartMovingWithSteering(steering, next_node)

    def visit_stop_moving(self, node) -> StopMovingNode:
        """Constructs the AST representation of the StopMoving node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return StopMovingNode(next_node)

    def visit_set_movement_speed(self, node) -> SetMovementSpeedNode:
        """Constructs the AST representation of the SetMovementSpeed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        value = self.visit_input(node["inputs"]["SPEED"][1])
        next_node = self.visit_node(node["next"])
        return SetMovementSpeedNode(value, next_node)

    def visit_set_motor_rotation(self, node) -> SetMotorRotationNode:
        """Constructs the AST representation of the SetMotorRotation node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        value = self.visit_input(node["inputs"]["DISTANCE"][1])
        unit = RotationUnit[node["fields"]["UNIT"][0].upper()]
        next_node = self.visit_node(node["next"])
        return SetMotorRotationNode(value, unit, next_node)

    def visit_start_animation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that animations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Animations are not supported yet, use the best_effort flag to generate code without animations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.",
            next_node,
        )

    def visit_play_animation_until_done(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that animations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Animations are not supported yet, use the best_effort flag to generate code without animations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.",
            next_node,
        )

    def visit_turn_on_for_duration(self, node) -> TurnOnForDurationNode:
        """Constructs the AST representation of the TurnOnForDuration node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        image = self.cst[node["inputs"]["MATRIX"][1]]["fields"][
            "field_flipperdisplay_custom-matrix"
        ][
            0
        ]  # TODO: Need to parse this
        duration = self.visit_input(
            node["inputs"]["VALUE"][1]
        )  # TODO: Need to visit this as if it where an value
        next_node = self.visit_node(node["next"])
        return TurnOnForDurationNode(image, duration, next_node)

    def visit_turn_on(self, node) -> TurnOnNode:
        """Constructs the AST representation of the TurnOn node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        image = self.cst[node["inputs"]["MATRIX"][1]]["fields"][
            "field_flipperdisplay_custom-matrix"
        ][0]
        next_node = self.visit_node(node["next"])
        return TurnOnNode(image, next_node)

    def visit_write(self, node) -> WriteNode:
        """Constructs the AST representation of the Write node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        text = self.visit_input(node["inputs"]["TEXT"][1])
        next_node = self.visit_node(node["next"])
        return WriteNode(text, next_node)

    def visit_turn_off_pixels(self, node) -> TurnOffPixelsNode:
        """Constructs the AST representation of the TurnOffPixels node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return TurnOffPixelsNode(next_node)

    def visit_set_pixel_brightness(self, node) -> SetPixelBrightnessNode:
        """Constructs the AST representation of the SetPixelBrightness node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        brightness = self.visit_input(node["inputs"]["BRIGHTNESS"][1])
        next_node = self.visit_node(node["next"])
        return SetPixelBrightnessNode(brightness, next_node)

    def visit_set_pixel_matrix_index(self, node) -> NumericalNode:
        return NumericalNode(float(node["fields"]["ledMatrixIndex"][0]))

    def visit_set_pixel(self, node) -> SetPixelNode:
        """Constructs the AST representation of the SetPixel node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        x = self.visit_input(node["inputs"]["X"][1])
        y = self.visit_input(node["inputs"]["Y"][1])
        brightness = self.visit_input(node["inputs"]["BRIGHTNESS"][1])
        next_node = self.visit_node(node["next"])
        return SetPixelNode(x, y, brightness, next_node)

    def visit_rotate_orientation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that rotations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Rotations are not supported yet, use the best_effort flag to generate code without rotations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.",
            next_node,
        )

    def visit_set_orientation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that rotations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Rotations are not supported yet, use the best_effort flag to generate code without rotations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.",
            next_node,
        )

    def visit_set_center_button(self, node) -> SetCenterButtonNode:
        """Constructs the AST representation of the SetCenterButton node.

        :param node: The Node representation.
        :return: The AST representation.
        """

        color_index = int(
            self.cst[node["inputs"]["COLOR"][1]]["fields"][
                "field_flipperdisplay_color-selector-vertical"
            ][0]
        )
        color = CenterButtonColor.at(color_index)
        next_node = self.visit_node(node["next"])
        return SetCenterButtonNode(color, next_node)

    def visit_light_up_distance_sensor(self, node) -> LightUpDistanceSensorNode:
        """Constructs the AST representation of the LightUpDistanceSensor node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        pattern = self.cst[node["inputs"]["VALUE"][1]]["fields"][
            "field_flipperdisplay_led-selector"
        ][0]
        next_node = self.visit_node(node["next"])
        return LightUpDistanceSensorNode(port, pattern, next_node)
