import os

import numpy as np

from rws2.RWS2 import RWS
from learning_from_demo.probabilistic_encoding import ProbabilisticEncoding
from learning_from_demo.gaussian_mixture_regression import GMR
from learning_from_demo.dynamical_movement_primitives import DynamicMovementPrimitives
from learning_from_demo.aligned_trajectories import AlignedTrajectories
from learning_from_demo.utility.dmp_visualization import plotting


if __name__ == "__main__":

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "demonstrations/app_simple",
    )
    trajectories = AlignedTrajectories.load_dataset_and_preprocess(data_dir)
    pe = ProbabilisticEncoding(
        trajectories, max_nb_components=10, min_nb_components=4, iterations=1
    )
    regression = GMR(trajectories, pe)
    dmp = DynamicMovementPrimitives(
        regression_fct=regression.prediction,
        alpha_z=18 * np.array([1, 1, 1, 1, 1, 1]),
        n_rfs=30,
        c_order=1,
    )
    # retrieve target goal (goal from camera, initial joints from robot)
    target = regression.prediction[-1, 1:]
    initial_state = regression.prediction[0, 1:]
    dmp_traj = dmp.compute_joint_dynamics(goal=target, y_init=initial_state)
    plotting(dmp)
    text = dmp_traj.joints_to_string()
    rws = RWS("https://localhost:8881")
    rws.upload_text_file_to_controller(text_data=text, filename="test.txt")
