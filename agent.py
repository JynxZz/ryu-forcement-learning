import os
import time
import yaml
import json
import argparse
import diambra.arena
from stable_baselines3 import PPO, A2C
from datetime import datetime
from diambra.arena.utils.gym_utils import show_gym_obs, show_wrap_obs, env_spaces_summary
#from stable_baselines3.common.buffers import Rollout_Buffer
import numpy as np
import sys
from make_sb3 import make_sb3_env

from stable_baselines3.common.callbacks import BaseCallback


class CustomCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """
    def __init__(self, verbose=0):
        super(CustomCallback, self).__init__(verbose)
        # Those variables will be accessible in the callback
        # (they are defined in the base class)
        # The RL model
        # self.model = None  # type: BaseAlgorithm
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env = None  # type: Union[gym.Env, VecEnv, None]
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = None  # type: Dict[str, Any]
        # self.globals = None  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger = None  # stable_baselines3.common.logger
        # # Sometimes, for event callback, it is useful
        # # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        pass

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass


RATIO = 0
WIDTH = 384
HEIGHT = 224

settings = {
    'player': 'P1',
    'step_ratio': 6,
    'frame_shape': [WIDTH, HEIGHT, 0],
    'continue_game': 0.0,
    'show_final': False,
    'hardcore': False,
    'difficulty': 8,
    'characters': [["Chun-Li"], ["Random"]],
    'action_space': 'multi_discrete',
    'attack_but_combination': True,
}
wrappers_settings={}
wrappers_settings["reward_normalization"] = True
wrappers_settings["flatten"] = True

if __name__ == "__main__":

    env, _ = make_sb3_env("sfiii3n", settings, wrappers_settings)
    agent = A2C("MultiInputPolicy", env , n_steps=1024)
    agent.learn(agent.n_steps)
    print(agent.rollout_buffer.observations)
    exit()


    # print(f"{agent.rollout_buffer._get_samples(np.array([[i for i in range(1024)]for j in range(4)]))}")
    #r_buffer = Rollout_Buffer()
    #agent.rollout_buffer = r_buffer
    observation = env.reset()

    step = 0
    while True:

        agent._last_obs = observation
        agent.collect_rollouts(env, CustomCallback(), agent.rollout_buffer, n_rollout_steps=1024)

        exit()
        # action, _state = agent.predict(observation, deterministic=True)
        # observation, reward, done, info = env.step(action)
        #buffer = agent.rollout_buffer.observations
        #agent.collect_rollouts(env, None, agent.rollout_buffer, n_rollout_steps=1024)
        # code pour enregistrer le buffer

#        agent.rollout_buffer.reset()
        # env.render()

        #action, _state = agent.predict(observation, deterministic=True)

        #observation, reward, done, info = env.step(action)
        # print(buffer)
        # if done:
        #     observation = env.reset()
        #     break

    env.close()
