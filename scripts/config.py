import random
class Configuration:

    def __init__(self):

        self.project = "nice-psyche-370808"
        self.bucket_path = "chun-li"

        # Evaluation
        self.eval_rounds = 2
        self.wait_time = random.random() * 6

        self.server_name = "gouki"
        self.clients_name = ["ryu", "ken", "osu", "honda", "guile", "blanka"]
        # self.clients_name = ["ryu"]

        # Environment settings
        self.env_settings = {
            'player': 'P1',
            'continue_game': 1.0,
            'show_final': False,  # If to show game final when game is completed
            'step_ratio': 6,  # Number of steps performed by the game # for every environment step, bounds: [1, 6]
            'difficulty': 8,
            'characters': [["Ryu"], ["Random"]],
            'frame_shape': [100, 100, 1],  # Native frame resize operation & 1=B&W
            'action_space': 'multi_discrete',  # 'multi_discrete'
            'attack_but_combination': True,
            'super_art': [0, 0],
            'hardcore': False,  # If to use hardcore mode in which observations are only made of game frame
            'rank': 1,  # ???
            'seed': -1,  # ???
            'grpc_timeout': 60  # ???
        }

        self.eval_settings = {
            'player': 'P1',
            'continue_game': 0.0,
            'show_final': False,  # If to show game final when game is completed
            'step_ratio': 6,  # Number of steps performed by the game # for every environment step, bounds: [1, 6]
            'difficulty': 8,
            'characters': [["Ryu"], ["Random"]],
            'frame_shape': [100, 100, 1],  # Native frame resize operation & 1=B&W
            'action_space': 'multi_discrete',  # 'multi_discrete'
            'attack_but_combination': True,
            'super_art': [0, 0],
            'hardcore': False,  # If to use hardcore mode in which observations are only made of game frame
            'rank': 1,  # ???
            'seed': -1,  # ???
            'grpc_timeout': 60  # ???
        }

        # Gym wrappers settings
        self.wrappers_settings = {
            "no_op_max": 0,  # Number of no-Op actions to be executed # at the beginning of the episode (0 by default)
            "sticky_actions": 1,  # Number of steps for which the same action should be sent (1 by default)
            "reward_normalization": True,  # When activated, the reward normalization factor can be set (default = 0.5)
            "reward_normalization_factor": 0.5,
            "frame_stack": 1,  # Number of frames to be stacked together (1 by default)
            "dilation": 1,  # Frames interval when stacking (1 by default)
            "actions_stack": 1,  # How many past actions to stack together (1 by default)
            "scale": False,  # If to scale observation numerical values (deactivated by default)
            "exclude_image_scaling": False,  # optionally exclude images from normalization (deactivated by default)
            "process_discrete_binary": False,
            # and optionally perform one-hot encoding also on discrete binary variables (deactivated by default)
            "scale_mod": 0,  # Scaling interval (0 = [0.0, 1.0], 1 = [-1.0, 1.0])
            "flatten": True,  # Flattening observation dictionary and filtering
            # "filter_keys": ["stage", "P1_ownSide", "P1_oppSide","P1_ownHealth", "P1_oppChar", "P1_actions_move", "P1_actions_attack"] # a sub-set of the RAM states
        }

    def init(self, name, **kwargs):
        """
        User-defined configuration init. Mandatory to properly set all configuration parameters.
        """

        self.name = name

        self.server = False
        if self.name == "gouki":
            self.server = True

        self.client = not self.server

        self.buffer_size = 2 ** 11
        if self.server:
            self.buffer_size *= 6

        self.buffer_path = f"{self.name}_obs.pickle"
        self.weights_path = "weights.zip"
        self.blob_path = f"{self.name}/{self.name}/"

        self.__dict__.update(kwargs)


CFG = Configuration()
