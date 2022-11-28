# DIAMBRA Arena module import
import diambra.arena
from IPython import display

# Environment creation
env = diambra.arena.make("sfiii3n")

# Environment reset
observation = env.reset()

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
