# DIAMBRA Arena module import
import diambra.arena
from diambra.arena.utils.gym_utils import show_gym_obs

# Environment creation
env = diambra.arena.make("sfiii3n")

# Environment reset
observation = env.reset()
show_gym_obs(observation=observation, n_actions_stack=env.n_act_stack, char_list=env.char_names, wait_key=1, viz=True)


# Agent-Environment interaction loop
while True:
    # (Optional) Environment rendering
    env.render()

    # Action random sampling
    actions = env.action_space.sample()
    # Environment stepping
    observation, reward, done, info = env.step(actions)

    # Episode end (Done condition) check
    if done:
        observation = env.reset()
        break

# Environment close
env.close()
