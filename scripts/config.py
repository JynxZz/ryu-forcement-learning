
class Configuration:
    """
    This configuration class is extremely flexible due to a two-step init process. We only instanciate a single instance of it (at the bottom if this file) so that all modules can import this singleton at load time. The second initialization (which happens in main.py) allows the user to input custom parameters of the config class at execution time.
    """

    def __init__(self):
        """
        Declare types but do not instanciate anything
        """

        self.project = "ryu-forcement-learning"
        self.bucket_path = "chun-li"

        # self.name = None

        # Evaluation
        self.eval_rounds = 3
        self.wait_time = 1

        self.server_name = "gouki"
        self.clients_name = ["ryu", "ken", "osu"]
        # self.clients_name = ["ryu", "ryu", "ryu"]

        # Environment settings
        self.env_settings = {
            'player': 'P1',
            'continue_game': 1.0,
            'show_final': False,  # If to show game final when game is completed
            'step_ratio': 6,  # Number of steps performed by the game # for every environment step, bounds: [1, 6]
            'difficulty': 8,
            'characters': [["Ryu"], ["Random"]],
            'frame_shape': [128, 128, 0],  # Native frame resize operation & 1=B&W
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
            'frame_shape': [128, 128, 0],  # Native frame resize operation & 1=B&W
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

        self.buffer_size = 64 # 2 ** 14
        if self.server:
            self.buffer_size *= 3

        self.buffer_path = f"{self.name}_obs.pickle"
        self.weights_path = "weights.zip"
        self.blob_path = f"{self.name}/{self.name}/"

        self.__dict__.update(kwargs)


CFG = Configuration()
