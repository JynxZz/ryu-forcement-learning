import random
class Configuration:
    """
    This configuration class is extremely flexible due to a two-step init process. We only instanciate a single instance of it (at the bottom if this file) so that all modules can import this singleton at load time. The second initialization (which happens in main.py) allows the user to input custom parameters of the config class at execution time.
    """

    def __init__(self):
        """
        Declare types but do not instanciate anything
        """
        self.bucket_path = "honda/"
        self.server_path = "honda/gouki/"
        self.weights = "weights.zip"
        self.obs = "_obs.pickle"

        self.rnd_seed = None
        self.agt_type = None


    def init(self, agt_type, **kwargs):
        """
        User-defined configuration init. Mandatory to properly set all configuration parameters.
        """

        # Mandatory arguments go here. In our case it is useless.
        self.agt_type = agt_type

        # We set default values for arguments we have to define
        self.rnd_seed = random.randint(0, 1000)
        self.epsilon = 0.05

        # However, these arguments can be overriden by passing them as keyword arguments in the init method. Hence, passing for instance epsilon=0.1 as a kwarg to the init method will override the default value we just defined.
        self.__dict__.update(kwargs)

        # Once all values are properly set, use them.
        random.seed(self.rnd_seed)


CFG = Configuration()

# import random
# import torch
# from turtle import shape
import json
import numpy as np
import mmap
# Environment settings
env_settings = {
  'player': 'P1',
  'continue_game': 1.0,
  'show_final': False, # If to show game final when game is completed
  'step_ratio': 6, # Number of steps performed by the game # for every environment step, bounds: [1, 6]
  'difficulty': 8,
  'characters': [["Ryu"], ["Random"]],
  'frame_shape': [128, 128, 0], # Native frame resize operation & 1=B&W
  'action_space': 'multi_discrete', # 'multi_discrete'
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
  "flatten": True, # Flattening observation dictionary and filtering
  #"filter_keys": ["stage", "P1_ownSide", "P1_oppSide","P1_ownHealth", "P1_oppChar", "P1_actions_move", "P1_actions_attack"] # a sub-set of the RAM states
  }

# array to list : arr_1.tolist()

#agent settings
# obs= {


# reward = float

result = {"env_settings" : env_settings,
          "wrappers_settings" : wrappers_settings,
        #   "observations" : obs
          }

result_json = json.dumps(result)

with open("settings.json", "w") as jsonfile:
    jsonfile.write(result_json)



print("Write successful")

#changer .json en .py

def json_to_py_start():
    with open("settings.json", "r") as jsonfile:

        data = json.load(jsonfile)
        env_settings = data["env_settings"]
        wrapper_settings = data["wrappers_settings"]

    # 2 premiers dicts settings & wrapper_settings
    return env_settings,wrapper_settings


# def json_to_py_agent()):
#     with open("settings.json", "r") as jsonfile:

#         data = json.load(jsonfile)
#         observations = data["observations"]

#     # dernier dict observations
#     return observations

# variable "serveur" = true or flase
is_server = True

# n_steps
n_steps = 100

# loop serve/client
looping = 4

# Waiting time
server_wait_time = 3
client_wait_time = 1
