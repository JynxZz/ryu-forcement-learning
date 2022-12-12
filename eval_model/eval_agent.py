from datetime import datetime

from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3 import A2C

from google.cloud import storage


import os
import json
import numpy as np

from config_eval import CFG

class EvalAgent:

    def __init__(self,
                 render=False,
                 agent_type=3,
                 agent_weights="weights_12h"):
        """
        Parameters
        ----------
        life : int, optional
            The number of lives the agent has. The default is 1.
        render : bool, optional
            Whether to render the environment. The default is False.
        agent_type : int, optional
            The type of agent. The default is 0.

        ----------
        """

        if agent_type == 3:
            self.env, _ = make_sb3_env("sfiii3n", CFG.settings, CFG.wrappers_settings)
            self.agent = A2C.load(agent_weights, env=self.env)

        self.render = render

        self.start_time = datetime.now()

    def iter_evaluate(self, agent_name, time=1) -> None:
        """
        This method iteratively evaluates an agent with a given name and number of iterations.
        It logs the results in a dictionary and writes the logs to a file.

        Parameters
        ----------
            agent_name (str): The name of the agent to evaluate.
            time (int): The number of times to evaluate the agent (default 1).

        Returns
        ----------
            None
        """
        logger = {}

        for i in range(time):
            logger[f'{agent_name}_{i + 1}'] = self.evaluate(3)

        self.write_logs(logger, agent_name)

    def custom_reward(self, stage, round_win, round_lost) -> tuple:
        """
        This function takes two parameters, stage and round_win and round_lost and returns a tuple containing the radius and cosinus.

        Parameters
        ----------
        stage (int): The stage of the game
        round_win (int): The number of rounds won
        round_lost (int): The number of rounds lost

        Returns
        ----------
        tuple:
            radius and cosinus
        """
        radius = stage * np.sqrt(round_win**2 + round_lost**2)
        cosinus = round_win / np.sqrt(round_win**2 + round_lost**2)
        return radius, cosinus

    def evaluate(self, agent_type) -> dict:
        """
        Evaluate the agent.

        Parameters
        ----------
        self : object
            The object of the class.
        render : bool
            If True, the environment is rendered.

        Returns
        ----------
        dict :
            A dictionary containing the evaluation results.
        ----------
        """

        round_count = 0
        stage = 1

        round_win = 0
        round_lost = 0
        timer = datetime.now()

        iter_steps = 0
        steps_round_won = []
        steps_round_lost = []

        env, _ = make_sb3_env("sfiii3n",  CFG.settings, CFG.wrappers_settings)

        if self.render:
            env.render()

        obs = env.reset()
        obs_before = obs.copy()

        while True:
            if agent_type == 1:
                actions = env.action_space.sample()
            elif agent_type == 3:
                actions, _ = self.agent.predict(obs, deterministic=False)

            obs, reward, done, info = env.step(actions)

            iter_steps += 1

            if info[0]['round_done'] and info[0]['stage_done']:
                round_count += 1
                round_win += 1
                stage += 1
                steps_round_won.append(iter_steps)
                iter_steps = 0

            elif info[0]['round_done'] and not info[0]['stage_done']:
                round_count += 1

                if obs_before['P1_oppHealth'] > obs_before['P1_ownHealth']:
                    round_lost += 1
                    steps_round_lost.append(iter_steps)
                    iter_steps = 0
                else:
                    round_win += 1
                    steps_round_won.append(iter_steps)
                    iter_steps = 0

            if done:
                total_time = datetime.now()
                break

            obs_before = obs.copy()

        env.close()

        radius, cosinus = self.custom_reward(stage, round_win, round_lost)

        return dict(start_time=self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    stage=stage,
                    round_total=round_count,
                    steps=info[0]['episode']['l'],
                    round_win=round_win,
                    steps_round_won=steps_round_won,
                    round_lost=round_lost,
                    steps_round_lost=steps_round_lost,
                    duration=str(total_time - timer),
                    reward=info[0]['episode']['r'],
                    radius=radius,
                    cosinus=cosinus)

    def write_logs(self, logs: dict, agent_name: str):
        """
        This function writes the logs to a json file.
        If the file does not exist, it creates one.
        If the file exists, it appends the logs to the existing file.

        Parameters:
        ----------
        logs (dict): The logs to be written to the file.
        agent_name (str): The name of the agent.

        Returns:
        ----------
        None
        ----------
        """
        if not os.path.exists(CFG.log_path):
            os.makedirs(CFG.log_path)
        if not os.path.exists(CFG.log_path + CFG.log_name.format(agent_name)):
            with open(CFG.log_path + CFG.log_name.format(agent_name), 'w') as f:
                json.dump(logs, f)
        else:
            with open(CFG.log_path + CFG.log_name.format(agent_name), 'r') as f:
                data = json.load(f)
            data.update(logs)
            with open(CFG.log_path + CFG.log_name.format(agent_name), 'w') as f:
                json.dump(data, f)

    def upload_eval(self, agent_name: str):
        client = storage.Client(CFG.project)
        bucket = client.bucket(CFG.bucket_path)
        blob = bucket.blob(f"{CFG.log_path + CFG.log_name.format(agent_name)}")
        blob.upload_from_filename(f"{CFG.log_path + CFG.log_name.format(agent_name)}")


if __name__ == '__main__':
    pass
