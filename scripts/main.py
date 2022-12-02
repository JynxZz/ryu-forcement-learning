import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

from scripts.config import *
from scripts.utils import *
from scripts.agent import *

from time import sleep

from config import CFG

# Instance Env
env, _ = make_sb3_env("sfiii3n", CFG.env_settings, CFG.wrappers_settings)


# Instance Agent
if CFG.agt_type == CFG.server:
    # WIP : when 3client : n_steps => 3 x n_steps
    server = AgentServer(env, n_steps=CFG.buffer_size)
else:
    client = AgentClient(env, n_steps=CFG.buffer_size)


i = 0
# LOOP
while i < CFG.looping:

    if CFG.agt_type == CFG.server:
        server.run()
        i += 1
        print(f'{i}# : Server')
    else:
        i += 1
        client.run()
        print(f'{i}# : Client')
