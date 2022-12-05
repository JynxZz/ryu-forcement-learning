import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

import agent

from config import CFG

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

CFG.init(args.name)

import tracemalloc
tracemalloc.start(10)


if CFG.server:
    server = agent.Server()
    server.run()
else:
    client = agent.Client()
    client.run()

snapshot = tracemalloc.take_snapshot()
statistics = snapshot.statistics('lineno')
print("[ Top 10 ]")
for stat in statistics[:10]:
    print(stat)


