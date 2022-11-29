
def start_settings():

    # Environment settings
    env_settings = {
        'player': 'P1',
        'continue_game': 0.0,
        'show_final': False, # If to show game final when game is completed
        'step_ratio': 6, # Number of steps performed by the game # for every environment step, bounds: [1, 6]
        'difficulty': 8,
        'characters': [["Ryu"], ["Random"]],
        'frame_shape': [512, 512, 0], # Native frame resize operation & 1=B&W
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
        "flatten": False, # Flattening observation dictionary and filtering
        #"filter_keys": ["stage", "P1_ownSide", "P1_oppSide","P1_ownHealth", "P1_oppChar", "P1_actions_move", "P1_actions_attack"] # a sub-set of the RAM states
        }

    # Discrete moves
    moves_discrete_dict={
        "no_move":0,
        "left":1,
        "left_jump":2,
        "jump":3,
        "right_jump":4,
        "right":5,
        "right_down":6,
        "down":7,
        "left_down":8,
        "attack_1":9,
        "attack_2":10,
        "attack_3":11,
        "attack_4":12,
        "attack_5":13,
        "attack_6":14,
        "attack_7":15,
        "attack_8":16,
        "attack_9":17,
        }

    # Multi-Discrete moves
    moves_multi_dict={
        "no_move & attack_1":[0,1]
        }

    return env_settings, wrappers_settings
