import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

from scripts.config import *
from scripts.utils import *
from scripts.agent import *

from time import sleep

# Load Settings & variables from config

env_settings, wrappers_settings = json_to_py_start()


# Instance Env
env, _ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)


# Instance Agent
if is_server:
    # WIP : when 3client : n_steps => 3 x n_steps
    server = AgentServer(env, n_steps=n_steps)

else:
    client = AgentClient(env, n_steps=n_steps)


# LOOP
i = 0
while i < looping:
    i += 1

    if server:
        while True:
            sleep(server_wait_time)
            init_timestamp, is_done = switch(server.init_timestamp)

            if is_done:
                buffer_1 = bucket_load("agent_one_obs.pickle")
                # buffer_2 = bucket_load("agent_two_obs.pickle")
                # buffer_3 = bucket_load("agent_three_obs.pickle")

                # TODO : Concat when more than 1 client
                # concat_buffer()

                server.compute(buffer_1, "new_weights")

                bucket_save("new_weights.zip")

                #TODO : Code evaluate method
                #server.evaluate()

                break

    if client:
        while True:
            client.game()

            client.write_buffer("agent_one_obs.pickle") # WIP : Variables

            bucket_save("agent_one_obs.pickle")

            while True:
                sleep(client_wait_time)
                init_timestamp, is_done = switch(client.init_timestamp)

                if is_done:
                    new_weights = bucket_load("new_weights.zip")

                    client.new_weights(f"{new_weights[:-4]}")
                    break
            break
