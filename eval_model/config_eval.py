class ConfigurationEval:
    """
    This class defines the Configuration class.
    It is used to define the configuration of the eval.

    Attributes
    ----------
        project: Name of the project. (str)
        bucket_path: Path of the bucket.  (str)
        eval_iter: Number of iterations for evaluation. (int)
        log_path: Path of the logs directory. (str)
        log_name: Name of the log file. (str)
        settings: Dictionary containing the settings for the env. (dict)
        wrappers_settings: Dictionary containing the wrapper settings for the env. (dict)
        agent_type: Dictionary containing the type of agent used for the eval. (dict)
        name: Name of the agent. (str)
        weights: Weights of the eval. (str)
        blob_path: Path of the blob. (str)

    Methods
    ----------
        __init__(): Initializes the Configuration class.
        init(): Initializes the configuration parameters.
    """

    def __init__(self):

        self.project = "nice-psyche-370808"
        self.bucket_path = "chun-li"

        self.eval_iter = 2

        self.log_path = "eval_model/logs/"
        self.log_name = "log_{}.json"

        self.settings = {
            'player': 'P1',
            'continue_game': 0,
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
            'seed': 0,  # ???
            'grpc_timeout': 60  # ???
        }

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
            "process_discrete_binary": False,  # and optionally perform one-hot encoding also on discrete binary variables (deactivated by default)
            "scale_mod": 0,  # Scaling interval (0 = [0.0, 1.0], 1 = [-1.0, 1.0])
            "flatten": True,  # Flattening observation dictionary and filtering
            # "filter_keys": ["stage", "P1_ownHealth", "P1_oppHealth"] # a sub-set of the RAM states
        }

        self.agent_type = {0: 'freeze',
                      1: 'random',
                      2: 'bot',
                      3: 'A2C',
                      4: 'PPO_Diambra'
        }

    def init(self, name="A2C", weights="weights_12h", **kwargs):

        self.name = name
        self.weights = weights

        self.blob_path = f"{self.name}/{self.weights}_eval/"

        self.__dict__.update(kwargs)


CFG = ConfigurationEval()
