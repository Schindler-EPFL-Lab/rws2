import time
from typing import Union

import numpy as np

from rws2 import RWS2


class RwsWrapper:
    def __init__(self, robot_url: str) -> None:
        """
        CLass constructor.
        :param robot_url: string that defines the robot url
        """
        self.robot = RWS2.RWS(robot_url)

    def set_RAPID_variable(
        self, variable_name: str, new_value: Union[float, int, str]
    ) -> None:
        """
        This method sets a RAPID variable to a new value. Both the variable name and
        the new value are passed by the user as method arguments. The user needs to
        request the controller mastership before changing the variable.
        :param variable_name: name of variable to update/change
        :param new_value: new variable value
        """
        self.robot.request_mastership()
        self.robot.set_rapid_variable(variable_name, new_value)
        self.robot.release_mastership()

    def turn_motors_on(self) -> None:
        """
        This method turns the robot motors on.
        """
        self.robot.request_mastership()
        self.robot.motors_on()
        self.robot.release_mastership()

    def activate_lead_through(self) -> None:
        """
        This method turns the motors on and activate the lead through mode.
        """
        self.turn_motors_on()
        self.robot.activate_lead_through()

    def deactivate_lead_through(self) -> None:
        """
        This method deactivates the lead through mode and switches off the robot motors.
        """
        self.robot.deactivate_lead_through()
        self.robot.motors_off()

    def complete_instruction(
        self, reset_pp: bool = False, var: str = "ready_flag"
    ) -> None:
        """
        This method sets up the robot, starts the RAPID program with a flag specifying
        if the program pointer needs to be reset and then it waits for the task
        completion. Finally, it stops the RAPID program and resumes the settings.
        :param reset_pp: boolean to determine if the program pointer needs to be reset
        :param var: RAPID variable that helps to synchronize the python script and the
                    RAPID program to achieve a coherent task execution
        """
        self.turn_motors_on()
        self.robot.start_RAPID(reset_pp)
        self.robot.wait_for_rapid()
        self.robot.stop_RAPID()
        self.set_RAPID_variable(var, "FALSE")

    def move_robot_linearly(self, pose: str, is_blocking: bool = True) -> None:
        """
        Loads the RAPID program linear_move.pgf (can be found in
        abb_controller_scripts)
        and sets the new value of the RAPID variable [pose]. Then it moves linearly to
        the defined pose.

        :param pose: string containing a list of list with the following robot
        information
        :param is_blocking: option to have the program waiting for the motion end
         [
         [x, y, z],
         [q1, q2, q3, q4],
         [cf1, cf4, cf6, cfx],
         [9e9, 9e9, 9e9, 9e9, 9e9, 9e9],
         ]
        """
        self.robot.upload_program_to_controller(
            prog_path="data/rapid_programs/linear_move/linear_move.pgf"
        )
        time.sleep(1)
        self.set_RAPID_variable(variable_name="pose", new_value=pose)
        self.robot.motors_on()
        self.robot.start_RAPID(pp_to_reset=True)
        while self.robot.is_running() and is_blocking:
            pass

    def execute_trajectory(self, goal_j: np.ndarray, is_blocking: bool = True) -> None:
        """
        Executes the dmp trajectory previously saved in the controller

        :param goal_j: target goal joints
        :param is_blocking: option to have the program waiting for the motion end
        """
        self.robot.upload_program_to_controller(
            prog_path="data/rapid_programs/joint_control_from_textfile/"
            "joint_control_from_textfile.pgf"
        )
        time.sleep(1)
        goal = str([goal_j.tolist(), [9e9, 9e9, 9e9, 9e9, 9e9, 9e9]])
        self.set_RAPID_variable(variable_name="joint_target", new_value=goal)
        self.robot.motors_on()
        self.robot.start_RAPID(pp_to_reset=True)
        while self.robot.is_running() and is_blocking:
            pass
        self.robot.motors_off()
