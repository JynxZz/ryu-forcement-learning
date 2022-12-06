import pickle
import time

from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C
from stable_baselines3.common.logger import configure

import utils
from config import CFG


class Agent:
    def __init__(self):
        self.env, _ = make_sb3_env("sfiii3n", CFG.env_settings, CFG.wrappers_settings)
        self.timestamp = time.time()
        # try :
        utils.download(utils.get_blob(CFG.server_name), CFG.weights_path)
        self.agent = A2C.load("weights", env=self.env)
        # except FileNotFoundError:
            # self.agent = A2C("MultiInputPolicy", self.env, n_steps=CFG.buffer_size)


class Client(Agent):

    def run(self):
        for _ in range(3):
            # Fill up replay buffer
            print("Step 1 -- go learn")
            self.agent.learn(total_timesteps=CFG.buffer_size)

            # Save buffer to pickle file
            print("Step 2 -- go save buffer")
            buffer = utils.extract_buffer(self.agent.rollout_buffer)
            print("Step 3 -- go write buffer")
            with open(CFG.buffer_path, "wb") as f:
                pickle.dump(buffer, f)
            self.agent.rollout_buffer.reset()

            # Upload buffer to bucket
            print("Step 4 -- go upload buffer")
            utils.upload(utils.get_blob(CFG.name), CFG.buffer_path)

            # Wait and load new weights
            print("Step 5 -- WAIT")
            utils.get_file_async(CFG.server_name, CFG.weights_path, self.timestamp)

            print("Step 6 -- new timestamp")
            self.timestamp = time.time()

            print("Step 7 -- load new weights and env")
            self.agent = A2C.load("weights", env=self.env)
            print("Step 8 -- reset")


class Server(Agent):

    def get_agent_obs(self, name):
        utils.get_file_async(name, f"{name}_obs.pickle", self.timestamp)
        with open(f"{name}_obs.pickle", "rb") as file:
            return pickle.load(file)

    def run(self):

        for _ in range(3):
            # Evaluate the agent and save results
            print("Step 1 - evaluate")
            score = self.evaluate()
            with open("reward.txt", "a") as file:
                file.write(f"{score}\n")

            # Wait for agent observations and load them
            print("Step 2 -- WAIT")
            buffers = [self.get_agent_obs(client) for client in CFG.clients_name]
            self.timestamp = time.time()
            print("Step 3 - reset timestamp")

            # Concatenate and load replay buffer
            print("Step 4 - Concat")
            buffer = utils.concat_buffers(buffers)

            print("Step 5 - Load buffer")
            self.agent.rollout_buffer = utils.load_buffer(buffer, self.agent.rollout_buffer)

            # Prepare buffer logging
            logg = configure(folder="/tmp/")
            self.agent.set_logger(logg)

            # Learn from loaded observations
            print("Step 6 - train")
            self.agent.train()

            # Save neural network weights and upload them on the bucket
            print("Step 7 - Save")
            self.agent.save(CFG.weights_path)
            utils.upload(utils.get_blob(CFG.name), CFG.weights_path)

            print("Step 8 - Reset")
            self.agent.rollout_buffer.reset()

    def evaluate(self) -> float:

        env, _ = make_sb3_env("sfiii3n", CFG.eval_settings, CFG.wrappers_settings)
        agent = A2C.load("weights", env=env)

        rew = [0 for _ in range(CFG.eval_rounds)]
        for eval_round in range(CFG.eval_rounds):
            obs = env.reset()
            while True:
                action, _ = agent.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                rew[eval_round] += reward[0]
                if done:
                    break
        env.close()
        agent.rollout_buffer.reset()
        return sum(rew) / len(rew)
