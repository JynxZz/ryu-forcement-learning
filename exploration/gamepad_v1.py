import os
from os.path import expanduser
import diambra.arena
from diambra.arena.utils.gamepad import DiambraGamepad


# Environment Settings
settings = {}
settings["player"] = "Random"
settings["step_ratio"] = 1
settings["frame_shape"] = [128, 128, 1]
settings["action_space"] = "multi_discrete"
settings["attack_but_combination"] = True

# Gym wrappers settings
wrappers_settings = {}
wrappers_settings["reward_normalization"] = True
wrappers_settings["frame_stack"] = 4
wrappers_settings["actions_stack"] = 12
wrappers_settings["scale"] = True


env = diambra.arena.make("sfiii3n", settings, wrappers_settings)

# GamePad(s) initialization
gamepad = DiambraGamepad()
gamepad.start()

observation = env.reset()

while True:

    env.render()

    actions = gamepad.get_actions()

    observation, reward, done, info = env.step(actions)

    if done:
        observation = env.reset()
        break

gamepad.stop()
env.close()
