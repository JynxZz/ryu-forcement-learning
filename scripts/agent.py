import pickle
import time

from multiprocessing import Pool

from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C
from stable_baselines3.common.logger import configure

import utils
from config import CFG


class Agent:
    def __init__(self, env):
        self.env = env
        self.agent = A2C("MultiInputPolicy", self.env, n_steps=CFG.buffer_size)
        self.timestamp = time.time()


class Client(Agent):
    def __init__(self, env):
        super().__init__(env)

    def run(self):

        while True:

            # Fill up replay buffer
            self.agent.learn(total_timesteps=CFG.buffer_size)

            # Save buffer to pickle file
            buffer = utils.extract_buffer(self.agent.rollout_buffer)
            with open(CFG.bucket_path, "wb") as f:
                pickle.dump(buffer, f)

            # Upload buffer to bucket
            utils.upload(utils.get_blob(CFG.name), CFG.buffer_path)

            # Wait and load new weights
            utils.get_file_async(CFG.server, CFG.weights_path, self.timestamp)
            self.timestamp = time.time()
            self.agent = A2C.load(CFG.weights_path)


class Server(Agent):
    def __init__(self, env):
        super().__init__(env)

    def get_agent_obs(self, name):
        utils.get_file_async(f"honda/{name}/", f"{name}_obs.pickle", self.timestamp)
        with open(f"{name}_obs.pickle", "rb") as file:
            return pickle.load(file)

    def run(self):

        while True:

            # Evaluate the agent and save results
            score = self.evaluate()
            with open("reward.txt", "a") as file:
                file.write(f"{score}\n")

            # Wait for agent observations and load them
            with Pool(3) as pool:
                buffers = pool.map(self.get_agent_obs, CFG.clients)
            self.timestamp = time.time()

            print("HEHEHEHEHE")
            print(len(buffers))
            exit(0)

            # Concatenate and load replay buffer
            buffer = utils.concat_buffers(buffers)
            self.agent.rollout_buffer = utils.load_buffer(buffer, self.agent.rollout_buffer)

            # Prepare buffer logging for some reason
            logg = configure(folder="/tmp/")
            self.agent.set_logger(logg)

            # Learn from loaded observations
            self.agent.train()

            # Save neural network weights and upload them on the bucket
            self.agent.save(CFG.weights)
            utils.upload(utils.get_blob(CFG.name), f"{CFG.weights}.zip")


    def evaluate(self) -> float:

        env, _ = make_sb3_env("sfiii3n", CFG.eval_settings, CFG.wrappers_settings)

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
        return sum(rew) / len(rew)