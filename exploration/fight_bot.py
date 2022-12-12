# Import
import diambra.arena
import pandas as pd
from random import randrange

env_settings = {
    'player': 'P1',
    'continue_game': 0.0,
    'show_final': True,  # If to show game final when game is completed
    'step_ratio': 1,  # Number of steps performed by the game # for every environment step, bounds: [1, 6]
    'difficulty': 8,
    'characters': [["Ryu"], ["Random"]],
    'frame_shape': [512, 512, 0],  # Native frame resize operation & 1=B&W
    'action_space': 'discrete',  # 'multi_discrete'
    'attack_but_combination': True,
    'super_art': [0, 0],
    'hardcore': False,  # If to use hardcore mode in which observations are only made of game frame
    'rank': 1,  # ???
    'seed': -1,  # ???
    'grpc_timeout': 60  # ???
}

wrappers_settings = {
            "no_op_max": 0,  # Number of no-Op actions to be executed # at the beginning of the episode (0 by default)
            "sticky_actions": 1,  # Number of steps for which the same action should be sent (1 by default)
            "reward_normalization": True,  # When activated, the reward normalization factor can be set (default = 0.5)
            "reward_normalization_factor": 0.5,
            "frame_stack": 1,  # Number of frames to be stacked together (1 by default)
            "dilation": 1,  # Frames interval when stacking (1 by default)
            "actions_stack": 1,  # How many past actions to stack together (1 by default)
            "scale": False,  # If to scale observation numerical values (deactivated by default)
            "exclude_image_scaling": True,  # optionally exclude images from normalization (deactivated by default)
            "process_discrete_binary": False,
            # and optionally perform one-hot encoding also on discrete binary variables (deactivated by default)
            "scale_mod": 0,  # Scaling interval (0 = [0.0, 1.0], 1 = [-1.0, 1.0])
            "flatten": True,  # Flattening observation dictionary and filtering
            "filter_keys": ["P1_ownSide", "P1_oppSide"] # a sub-set of the RAM states
        }

# Environment set and observation reset
env = diambra.arena.make("sfiii3n", env_settings=env_settings,wrappers_settings=wrappers_settings)
observation = env.reset()
observation_all=[]
reward_all=[]

# Liste des combos
Hadouken_right=[7,6,5,10]
Hadouken_left=[7,8,1,10]
Tatsumaki_right=[7,6,5,13]
Tatsumaki_left=[7,8,1,13]
Sliding_high_kick_left=[1,8,7,6,5,13]
Sliding_high_kick_right=[5,6,7,8,1,14]
Super_fireball_right=[7,6,5,7,6,5,9]
Super_fireball_=[7,8,1,7,8,1,10]
Shoryuken_right=[5,6,7,10]
Shoryuken_left=[1,8,7,10]

done = False

while  len(reward_all) <= 10000000:

    if observation["P1_ownSide"] == 0:

        for step in Hadouken_right:
            env.render(mode="human")
            if not done:
                observation, reward, done, info = env.step(step)
                reward_all.append(reward)
            else:
                pass

    else:

        for step in Hadouken_left:
            env.render(mode="human")
            if not done:
                observation, reward, done, info = env.step(step)
                reward_all.append(reward)
            else:
                pass

    if done:
        break

outputs=pd.DataFrame({"reward_all":reward_all})
outputs.to_csv('outputs.csv')

# Environment close
env.close()
