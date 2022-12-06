# Import
import diambra.arena
import pandas as pd
from random import randrange


env_settings = {
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


wrappers_settings = {
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


# Environment set and observation reset
env = diambra.arena.make("sfiii3n", env_settings=env_settings,wrappers_settings=wrappers_settings)
observation = env.reset()
observation_all=[]
reward_all=[]
done_all=[]
info_all=[]


# Agent-Environment interaction loop
while  len(reward_all) <= 1000:

    # Environment rendering --> mode = "human","rgb_array"
    env.render(mode="human")

    # Action random sampling // to-do plug l'AGENT
    actions= randrange(9,15)

    # Environment stepping
    observation, reward, done, info = env.step(actions)

  """   # Environment visualization
    print("-----observation-----")
    print(observation)
    print("-----reward----------")
    print(reward)
    print("-----done------------")
    print(done)
    print("-----info------------")
    print(info)
    print("-----step------------")
    print(len(reward_all)+1)

    # Environment manual recording
    observation_all.append(observation)
    reward_all.append(reward)
    done_all.append(done)
    info_all.append(info)

    # In case, Ryu wins the game --> restart a tournament without braking
    if done:
        env = diambra.arena.make("sfiii3n", env_settings=env_settings,wrappers_settings=wrappers_settings)
        env.render(mode="human")
        actions= randrange(9,11)
        observation, reward, done, info = env.step(actions)

            # Environment visualization
        print("-----observation-----")
        print(observation)
        print("-----reward----------")
        print(reward)
        print("-----done------------")
        print(done)
        print("-----info------------")
        print(info)
        print("-----step------------")
        print(len(reward_all)+1)

        # Environment manual recording
        observation_all.append(observation)
        reward_all.append(reward)
        done_all.append(done)
        info_all.append(info)

# Save and csv
outputs=pd.DataFrame({
    "observation":observation_all,
    "reward":reward_all,
    "done":done_all,
    "info":info_all})
outputs.to_csv('outputs.csv') """

# Environment close
env.close()
