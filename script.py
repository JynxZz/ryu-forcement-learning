# DIAMBRA Arena module import
import diambra.arena
import pandas as pd

# Environment creation

env_settings = {
    'player': 'P1',
    'continue_game': 0.0,
    'show_final': False,
    'step_ratio': 1,
    'difficulty': 8,
    'characters': [["Ryu"], ["Random"]],
    'frame_shape': [512, 512, 0], #512 & 1=B&W
    'action_space': 'discrete', # 'multi_discrete'
    'attack_but_combination': True,
    'super_art':[0,0],
    'hardcore': False,
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
    "actions_stack":12, # How many past actions to stack together (1 by default)
    "scale": True, # If to scale observation numerical values (deactivated by default)
    "exclude_image_scaling": True, # optionally exclude images from normalization (deactivated by default)
    "process_discrete_binary": True, # and optionally perform one-hot encoding also on discrete binary variables (deactivated by default)
    "scale_mod": 0 # Scaling interval (0 = [0.0, 1.0], 1 = [-1.0, 1.0])
}


# Flattening observation dictionary and filtering
# a sub-set of the RAM states
wrappers_settings["flatten"] = True
wrappers_settings["filter_keys"] = ["stage", "P1_ownSide", "P1_oppSide",
                                    "P1_ownHealth", "P1_oppChar",
                                    "P1_actions_move", "P1_actions_attack"]


#env = diambra.arena.make("sfiii3n", env_settings=env_settings)
env = diambra.arena.make("sfiii3n", env_settings)

# Environment reset
observation = env.reset()

# Agent-Environment interaction loop
observation_all=[]
reward_all=[]
done_all=[]
info_all=[]

while True:
    # (Optional) Environment rendering --> mode = "human","rgb_array"
    env.render(mode="human")

    # Action random sampling
    #actions = env.action_space.sample()
    moves_discrete_dict={"no_move":0,
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
    moves_multi_dict={"no_move & attack_1":[0,1]}
    actions= 1
    # Environment stepping
    observation, reward, done, info = env.step(actions)

    print("-----observation-----")
    print(observation)
    print("-----reward----------")
    print(reward)
    print("-----done------------")
    print(done)
    print("-----info------------")
    print(info)

    # Environment manual recording
    observation_all.append(observation)
    reward_all.append(reward)
    done_all.append(done)
    info_all.append(info)

    print("-----step------------")
    print(len(reward_all))

    # Episode end (Done condition) check
    if done:
        outputs=pd.DataFrame({
                        "observation":observation_all,
                        "reward":reward_all,
                        "done":done_all,
                        "info":info_all})

        outputs.to_csv('outputs.csv')

        #observation = env.reset()
        break

# Environment close
env.close()
