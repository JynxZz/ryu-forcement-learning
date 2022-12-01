import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

from scripts.config import *
from scripts.utils import *
from scripts.agent import *

from time import sleep

from config import CFG

# Load Settings & variables from config
env_settings, wrappers_settings = json_to_py_start()

# Instance Env
env, _ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)

project = os.environ['PROJECT']
bucket = os.environ['BUCKET_TEST']
agent_name = os.environ['AGENT_NAME']
file_name = os.environ['OBS']
compute_name = os.environ['NEW_WEIGHTS']

is_server=False
# Instance Agent
if is_server:
    # WIP : when 3client : n_steps => 3 x n_steps
    server = AgentServer(env, n_steps=n_steps)
else:
    client = AgentClient(env, n_steps=n_steps)


i = 0
# LOOP
while i < looping:

    if is_server:
        server.run(project, bucket, agent_name, file_name, False, compute_name)
        i += 1
        print(f'{i}# : Server')
    else:
        i += 1
        client.run(project, bucket, agent_name, file_name, True, compute_name)
        print(f'{i}# : Client')
