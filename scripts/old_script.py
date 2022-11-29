import diambra.arena
from datetime import datetime
from diambra.arena.utils.gym_utils import show_gym_obs, show_wrap_obs, env_spaces_summary
from IPython import display
import numpy as np
import sys
from helper import plot


############
# SETTINGS #
############
RATIO = 0
WIDTH = 384
HEIGHT = 224

settings = {
    'player': 'P1',
    'step_ratio': 6,
    'frame_shape': [RATIO, RATIO, 0],
    'continue_game': 0.0,
    'show_final': False,
    'hardcore': False,
    'difficulty': 8,
    'characters': [["Chun-Li"], ["Random"]],
    'action_space': 'multi_discrete',
    'attack_but_combination': True,
    'env_address':'127.0.0.1:49182',
}

##########################
# REINFORCEMENT LEARNING #
##########################

env = diambra.arena.make("sfiii3n", settings)

observation = env.reset()

show_gym_obs(observation, env.char_names)

# env_spaces_summary(env=env)
# show_wrap_obs(observation=observation, n_actions_stack=env.n_act_stack, char_list=env.char_names, wait_key=1, viz=True)
i = 1


######################
# SETUP VAR AND RUN  #
######################

sys.stdout = open('log.txt', 'w')
start_time = datetime.now()

plot_time = []
plot_reward = []
total_reward = 0
round_count = 0

print('=' * 30)
print("Start Learning")
print("Rounds: {}".format(round_count))
print("Total Reward: {}".format(total_reward))
print('Start at: {}'.format(start_time))
print('=' * 30)


while True:

    env.render()

    actions = env.action_space.sample()

    observation, reward, done, info = env.step(actions)
    # show_gym_obs(observation, env.char_names)


    timer = datetime.now()
    plot_time.append(timer)
    plot_reward.append(reward)
    total_reward += reward

    if info['round_done'] == True:
        round_count += 1

        print('=' * 30)
        print("Rounds: {}".format(round_count))
        print("Continue: {}".format(-(settings['continue_game'])))
        print("Total Reward: {}".format(total_reward))
        print('Time: {}'.format(timer - start_time))
        print("Info: {}".format(info))
        print('=' * 30)

        # plot(plot_time, np.mean(plot_reward))

        if done:
            observation = env.reset()

            show_gym_obs(observation, env.char_names)

            total_time = datetime.now()

            print('=' * 30)
            print("Rounds: {}".format(round_count))
            print("Rewards: {}".format(plot_reward))
            print("Total Reward: {}".format(total_reward))
            print("Done: {}".format(done))
            print('Duration: {}'.format(total_time - start_time))
            print("Info: {}".format(info))
            print('=' * 30)

            break
env.close()
sys.stdout.close()
