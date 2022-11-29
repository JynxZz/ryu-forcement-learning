import random
from turtle import shape
import torch
import json
import numpy as np
#changer dict clement en json sur settings.json
env_settings = {
  'player': 'P1',
  'continue_game': 1.0,
  'show_final': False, # If to show game final when game is completed
  'step_ratio': 6, # Number of steps performed by the game # for every environment step, bounds: [1, 6]
  'difficulty': 8,
  'characters': [["Ryu"], ["Random"]],
  'frame_shape': [512, 512, 0], # Native frame resize operation & 1=B&W
  'action_space': 'discrete', # 'multi_discrete'
  'attack_but_combination': True,
  'super_art':[0,0],
  'hardcore': False, # If to use hardcore mode in which observations are only made of game frame
  'rank':1,                           #???
  'seed':-1,                          #???
  'grpc_timeout':60                   #???
  }

# Gym wrappers settings
wrappers_settings = {
  "no_op_max" : 0, # Number of no-Op actions to be executed # at the beginning of the episode (0 by default)
  "sticky_actions" : 1, # Number of steps for which the same action should be sent (1 by default)
  "reward_normalization": True, # When activated, the reward normalization factor can be set (default = 0.5)
  "reward_normalization_factor": 0.5,
  "frame_stack": 1, # Number of frames to be stacked together (1 by default)
  "dilation":1, # Frames interval when stacking (1 by default)
  "actions_stack":1, # How many past actions to stack together (1 by default)
  "scale": False, # If to scale observation numerical values (deactivated by default)
  "exclude_image_scaling": False, # optionally exclude images from normalization (deactivated by default)
  "process_discrete_binary": False, # and optionally perform one-hot encoding also on discrete binary variables (deactivated by default)
  "scale_mod": 0, # Scaling interval (0 = [0.0, 1.0], 1 = [-1.0, 1.0])
  "flatten": False, # Flattening observation dictionary and filtering
  #"filter_keys": ["stage", "P1_ownSide", "P1_oppSide","P1_ownHealth", "P1_oppChar", "P1_actions_move", "P1_actions_attack"] # a sub-set of the RAM states
  }


# obs= {
#     'observations': {
#     'P1_actions_attack': torch.tensor([[0.],[8.],[2.],[7.],[5.]]),
#     'P1_actions_move': torch.tensor([[0.],[6.],[1.],[1.],[4.]]),
#     'P1_oppChar': torch.tensor([[9.],[9.],[9.],[9.],[9.]]),
#     'P1_oppChar1': torch.tensor([[9.],[9.],[9.],[9.],[9.]]),
#     'P1_oppHealth': torch.tensor([[160.],[160.],[160.],[160.],[160.]]),
#     'P1_oppSide': torch.tensor([[1.],[1.],[1.],[1.],[1.]]),
#     'P1_oppStunBar': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_oppStunned': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_oppSuperBar': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_oppSuperCount': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_oppSuperMaxCount': torch.tensor([[1.],[1.],[1.],[1.],[1.]]),
#     'P1_oppSuperType': torch.tensor([[1.],[1.],[1.],[1.],[1.]]),
#     'P1_oppWins': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_ownChar': torch.tensor([[7.],[7.],[7.],[7.],[7.]]),
#     'P1_ownChar1': torch.tensor([[7.],[7.],[7.],[7.],[7.]]),
#     'P1_ownHealth': torch.tensor([[160.],[160.],[160.],[160.],[160.]]),
#     'P1_ownSide': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_ownStunBar': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_ownStunned': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_ownSuperBar': torch.tensor([[0.],[0.],[2.],[2.],[2.]]),
#     'P1_ownSuperCount': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'P1_ownSuperMaxCount': torch.tensor([[3.],[3.],[3.],[3.],[3.]]),
#     'P1_ownSuperType': torch.tensor([[2.],[2.],[2.],[2.],[2.]]),
#     'P1_ownWins': torch.tensor([[0.],[0.],[0.],[0.],[0.]]),
#     'frame': torch.tensor(([random.uniform(0.,255.) for _ in range(3*244*384)])),
#     'stage': torch.tensor([[1.],[1.],[1.],[1.],[1.]])},
#     'actions':torch.tensor([[6., 8.],[1., 2.],[1., 7.],[4., 5.],[1., 7.]]),
#     'old_values':torch.tensor([-0.1244, -0.0768, -0.0817, -0.1098, -0.0945]),
#     'old_log_prob':torch.tensor([-4.5106, -4.5129, -4.5209, -4.4947, -4.5208]),
#     'advantages':torch.tensor([ 0.0357, -0.0128, -0.0088,  0.0184,  0.0021]),
#     'returns':torch.tensor([-0.0887, -0.0896, -0.0905, -0.0914, -0.0923])}

# reward = float

result = {"env_settings" : env_settings,
          "wrappers_settings" : wrappers_settings,
        #   "observations" : obs
          }

result_json = json.dumps(result)

with open("settings.json", "w") as jsonfile:
    jsonfile.write(result_json)



print("Write successful")

# #changer .json en .py

def json_to_py_start(filename):
    with open("settings.json", "r") as jsonfile:

        data = json.load(jsonfile)
        env_settings = data["env_settings"]
        wrapper_settings = data["wrappers_settings"]

    # 2 premiers dicts settings & wrapper_settings
    return env_settings,wrapper_settings


# def json_to_py_agent(filename):
#     with open("settings.json", "r") as jsonfile:

#         data = json.load(jsonfile)
#         observation = data["observations"]

#     # dernier dict observations
#     return observation
