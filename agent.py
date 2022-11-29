import os
import diambra.arena
from stable_baselines3 import PPO, A2C
import pickle
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3.common.logger import configure
import numpy as np

"""
    Settings editable
"""
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

    # Creation of environment from diambra
    env, _ = make_sb3_env("sfiii3n", settings, wrappers_settings)

    # Instancing Agent Agent("Policy", environment, n_steps)
    agent = A2C("MultiInputPolicy", env , n_steps=1000)
    #total_timesteps(<= n_steps so it doesn't learn)
    agent.learn(total_timesteps= agent.n_steps)
    #saving parameters in 'weights.zip' (139Mo)
    agent.save("weights")
    #Extracting buffer
    buffer = agent.rollout_buffer

    #Training another agent (called 'test') from one's buffer
    test = A2C("MultiInputPolicy", env , n_steps=1024)
    test.rollout_buffer=buffer
    logg = configure(folder='/tmp/')
    test.set_logger(logg)
    test.train()

    #Loading an agent from imported parameters (here in '/weights.zip')
    sec = A2C.load('weights')


    exit()
