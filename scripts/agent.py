import datetime
import pickle
import time

import numpy as np
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C
from stable_baselines3.common.logger import configure

import scripts.utils as utils
from scripts.config import CFG, env_settings, wrappers_settings


class Agent:
    def __init__(self, env):
        self.env = env
        self.agent = A2C("MultiInputPolicy", self.env, n_steps=CFG.buffer_size)

        self.init_timestamp = time.time()


class Server(Agent):
    def __init__(self, env):
        super().__init__(env)

    def evaluate(self) -> float:

        # TODO Have a separate eval env in CFG
        env_settings["continue_game"] = 0
        env, _ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)

        # TODO Remove when CFG clean
        CFG.eval_rounds = 3

        rew = [0 for _ in CFG.eval_rounds]
        for eval_round in range(CFG.eval_rounds):
            obs = env.reset()
            while True:
                action, _ = self.agent.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                rew[eval_round] += reward[0]
                if done:
                    break
        env.close()
        env_settings["continue_game"] = 1
        return sum(rew) / len(rew)

    def run(self):

        i = 0
        while True:

            time.sleep(CFG.wait_time)
            blob = utils.get_blob_client()
            try:
                blob_time = utils.get_timestamp(blob)
            except:
                blob_time = 0

            if self.init_timestamp < blob_time:
                # TODO Multithread
                # TODO Ecrire fonction get_buffers_async
                buffer_ryu = utils.download(blob, CFG.path_ryu)
                # buffer_ken = utils.download(blob, CFG.path_ken)
                # buffer_osu = utils.download(blob, CFG.path_osu)

                # TODO : Deuxième fonction, prepare buffers

                # 2.1. Load files from pickles
                with open(CFG.obs_ryu, "rb") as f:
                    obs_ryu = pickle.load(f)

                # TODO : Concat when more than 1 client
                # 2.2. Concat pickles
                # concat_obs = concat_buffer([obs_ryu, obs_ken, obs_osu])

                # 2.3. Load the concat buffer
                self.agent.rollout_buffer = utils.load_buffer(
                    obs_ryu, self.agent
                )  # TODO: no return inside method

                # 2.4. Prep buffer logging
                logg = configure(folder="/tmp/")
                self.agent.set_logger(logg)

                # Step 3 - Compûte weights
                self.agent.train()

                # Saving parameters in 'weights.zip' (139Mo)
                self.agent.save(CFG.weights[:-4])

                blob = utils.get_blob_server()
                utils.upload(blob, CFG.weights)

                # Evaluate
                score = self.evaluate()

                with open("reward.txt", "a") as file:
                    file.write(f"{i} \t {CFG.buffer_size} \t {score}\n")

                i += 1
                print(f"{i}# : Server")


# CLIENT
class Client(Agent):
    def __init__(self, env):
        super().__init__(env)

    def game(self):
        self.agent.learn(total_timesteps=CFG.buffer_size)

    def write_buffer(self):
        to_buffer = utils.extract_buffer(self.agent)

        with open(f"{CFG.name+CFG.obs}", "wb") as f:
            pickle.dump(to_buffer, f)

    def new_weights(self):
        self.agent = A2C.load(CFG.obs)

    def run(self):

        i = 0
        while True:
            self.game()

            self.write_buffer()

            blob = utils.get_blob_client()
            utils.upload(blob, f"{CFG.name+CFG.obs}")

            while True:
                time.sleep(CFG.wait_time)

                blob = utils.get_blob_server()

                try:

                    blob_time = utils.get_timestamp(blob)
                except:
                    blob_time = 0

                if self.init_timestamp < blob_time:
                    uploading = False
                    blob = utils.get_blob_server()
                    utils.download(blob, CFG.weights)

                    self.new_weights(f"{CFG.weights[:-4]}")

                    break

            i += 1
            print(f"{i}# : Client")
