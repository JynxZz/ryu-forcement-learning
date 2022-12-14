import pickle
import time

from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C
from stable_baselines3.common.logger import configure
from google.api_core.exceptions import NotFound

import utils
from config import CFG


class Agent:
    def __init__(self):
        self.env, _ = make_sb3_env("sfiii3n", CFG.env_settings, CFG.wrappers_settings)
        self.timestamp = time.time()
        try :
            utils.download(utils.get_blob(CFG.server_name), CFG.weights_path)
            self.agent = A2C.load("weights", env=self.env)
        except (FileNotFoundError, NotFound):
            self.agent = A2C("MultiInputPolicy", self.env, n_steps=CFG.buffer_size)


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
            time.sleep(CFG.wait_time)
            self.agent = A2C.load("weights", env=self.env)
            print("Step 8 -- reset")


class Server(Agent):

    def get_agent_obs(self, name):
        utils.get_file_async(name, f"{name}_obs.pickle", self.timestamp)
        with open(f"{name}_obs.pickle", "rb") as file:
            return pickle.load(file)

    def run(self):

        # for _ in range(3):
        # Evaluate the agent and save results

        # Wait for agent observations and load them
        print("Step 1 -- WAIT")
        buffers = [self.get_agent_obs(client) for client in CFG.clients_name]

        print("Step 2 - reset timestamp")
        self.timestamp = time.time()


        # Concatenate and load replay buffer
        print("Step 3 - Concat")
        buffer = utils.concat_buffers(buffers)

        print("Step 4 - Load buffer")
        self.agent.rollout_buffer = utils.load_buffer(buffer, self.agent.rollout_buffer)

        # Prepare buffer logging
        logg = configure(folder="/tmp/")
        self.agent.set_logger(logg)

        # Learn from loaded observations
        print("Step 5 - train")
        self.agent.train()

        # Save neural network weights and upload them on the bucket
        print("Step 6 - Save")
        self.agent.save(CFG.weights_path)
        utils.upload(utils.get_blob(CFG.name), CFG.weights_path)

        print("Step 7 - evaluate")
        score = self.evaluate()
        with open("reward.txt", "a") as file:
            file.write(f"{score}\n")

        print("Step 8 - Reset")
        self.agent.rollout_buffer.reset()

    def evaluate(self) -> float:

        env, _ = make_sb3_env("sfiii3n", CFG.eval_settings, CFG.wrappers_settings)
        agent = A2C.load("weights", env=env)

        rew = []
        obs = env.reset()
        while True:
            action, _ = agent.predict(obs, deterministic=False)
            obs, reward, done, _ = env.step(action)
            rew.append(reward[0])
            if done:
                break
        env.close()
        agent.rollout_buffer.reset()
        del agent, env, _
        return f"{sum(rew)} \t {len(rew)}"
