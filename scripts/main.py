import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

import scripts.agent as agent

from config import CFG

import argparse
args = argparse.ArgumentParser().add_argument("name").parse_args()

CFG.init(args.name)

env, _ = make_sb3_env("sfiii3n", CFG.env_settings, CFG.wrappers_settings)

if CFG.name == CFG.server:
    server = agent.Server(env)
    server.run()
else:
    client = agent.Client(env)
    client.run()
