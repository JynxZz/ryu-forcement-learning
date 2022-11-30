# Import
import diambra.arena
import pandas as pd
from random import randrange
from scripts.config import json_to_py_start


# Environment set and observation reset
env_settings, wrappers_settings=json_to_py_start()
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

    # Action random sampling
    actions= randrange(9,11)
    """ actions = 9 """

    # Environment stepping
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
outputs.to_csv('outputs.csv')

# Environment close
env.close()
