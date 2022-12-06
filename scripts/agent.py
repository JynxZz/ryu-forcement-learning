from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C
from stable_baselines3.common.logger import configure

import utils
from config import CFG
from file import File


class Agent:
    def __init__(self):

        self.name = CFG.name
        self.weight_file = File("weights.zip")
        self.buffer_files = {name: File(f"{name}_obs.pickle") for name in CFG.clients_name}

        self.env, _ = make_sb3_env("sfiii3n", CFG.env_settings, CFG.wrappers_settings)
        self.agent = A2C("MultiInputPolicy", self.env, n_steps=CFG.buffer_size)
        if self.weight_file.exists():
            self.weight_file.download()
            self.agent.load("weights", env=self.env)


class Client(Agent):

    def __init__(self):
        super().__init__()
        self.name = CFG.name
        self.buffer_file: File = self.buffer_files[self.name]

    def run(self):
        for _ in range(3):
            print("1. Filling replay buffer")
            self.agent.learn(total_timesteps=CFG.buffer_size)

            print("2. Saving buffer to file")
            buffer = utils.extract_buffer(self.agent.rollout_buffer)
            self.buffer_file.to_pickle(buffer)
            self.agent.rollout_buffer.reset()

            print("3. Uploading buffer to bucket")
            self.buffer_file.upload()

            print("4. Waiting for new weights")
            self.weight_file.get_update()

            print("5. Loading new weights")
            self.weight_file.download()
            self.agent = A2C.load("weights", env=self.env)


class Server(Agent):

    def run(self):

        for _ in range(3):

            # Evaluate the agent and save results
            print("Step 1 - evaluate")
            score = self.evaluate()
            with open("reward.txt", "a") as file:
                file.write(f"{score}\n")

            print("2. Waiting for replay buffers")
            for buffer_blob in self.buffer_files:
                buffer_blob.get_update()
                buffer_blob.download()

            print("3. Loading replay buffers")
            buffers = [buffer.from_pickle() for buffer in self.buffer_files]
            buffer = utils.concat_buffers(buffers)
            self.agent.rollout_buffer = utils.load_buffer(buffer, self.agent.rollout_buffer)
            logg = configure(folder="/tmp/")
            self.agent.set_logger(logg)

            print("4. Training")
            self.agent.train()

            print("5. Saving new weights")
            self.agent.save(self.weight_file.path)
            self.weight_file.upload()

            print("6. Resetting agent")
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
