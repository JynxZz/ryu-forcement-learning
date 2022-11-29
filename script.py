# DIAMBRA Arena module import
import diambra.arena
import pandas as pd
from random import randrange
from settings import start_settings

# Environment set and observation reset
env_settings, wrappers_settings=start_settings()
env = diambra.arena.make("sfiii3n", env_settings=env_settings,wrappers_settings=wrappers_settings)
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
    actions= [2,randrange(1,5)]

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
