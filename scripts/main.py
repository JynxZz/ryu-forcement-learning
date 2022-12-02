import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
import sys
import scripts.config as config
import scripts.utils as utils
import scripts.agent as agent

from time import sleep

from config import CFG

# TODO INIT THE CFG CONFIG HERE
CFG.init(...)

# TODO Move this to config
env_settings, wrappers_settings = json_to_py_start()

# TODO Move this to config
project = os.environ['PROJECT']
bucket = os.environ['BUCKET_TEST']
agent_name = os.environ['AGENT_NAME']
file_name = os.environ['OBS']
compute_name = os.environ['NEW_WEIGHTS']

env, _ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)

if CFG.server:
    server = agent.Server(env)
    server.run(project, bucket, agent_name, file_name, False, compute_name)
else:
    client = agent.Client(env)
    client.run(project, bucket, agent_name, file_name, True, compute_name)
