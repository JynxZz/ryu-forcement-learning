from stable_baselines3 import A2C
import datetime
import time
import pickle
import numpy as np


from stable_baselines3.common.logger import configure
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env


from scripts.config import CFG
import scripts.utils as utils
from scripts.config import env_settings, wrappers_settings


class Agent():

        def __init__(self, env, n_steps):
            self.env = env
            self.n_steps = n_steps
            self.agent = A2C("MultiInputPolicy", self.env , n_steps= self.n_steps)
            self.init_timestamp = time.time()


class Server(Agent):

    def __init__(self,  env, n_steps):
        super().__init__(env, n_steps)
        self.name = "server"

    def evaluate(self) -> float:

        # TODO Have a separate eval env in CFG
        env_settings['continue_game']=0
        env,_ = make_sb3_env("sfiii3n", env_settings, wrappers_settings)

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
        env_settings['continue_game']=1
        return sum(rew)/len(rew)

    def run(self, project, bucket, agent_name, file_name, uploading, compute_name):

        server_wait_time = 1

        i = 0
        while True:

            time.sleep(server_wait_time)
            #init_timestamp, is_done = switch(self.init_timestamp)
            blob = utils.interface_bucket(project, bucket, agent_name, file_name)

            try:
                # is_done=switch(blob, self.init_timestamp)
                blob_time = utils.get_timestamp(blob)
            except:
                blob_time = 0

            if self.init_timestamp < blob_time:
                # buffer_1 = upload_download(blob, agent_name, file_name, uploading)
                # TODO Multithread
                # TODO Ecrire fonction get_buffers_async
                buffer_1 = utils.max_download(blob, f"{agent_name+file_name}")
                # buffer_2 = bucket_load("agent_two_obs.pickle")
                # buffer_3 = bucket_load("agent_three_obs.pickle")

                # TODO Deuxième fonction, prepare buffers

                # 2.1. Load files from pickles
                with open(f"{agent_name+file_name}", 'rb') as f:
                    obs = pickle.load(f)
                # TODO : Concat when more than 1 client
                # 2.2. Concat pickles
                # concat_buffer(obs_1, obs_2, obs_3)

                # 2.3. Load the concat buffer
                self.agent.rollout_buffer = utils.load_buffer(obs, self.agent) # TODO: no return inside method

                # 2.4. Prep buffer logging
                logg = configure(folder='/tmp/')
                self.agent.set_logger(logg)

                # Step 3 - Compûte weights
                self.agent.train()

                #Saving parameters in 'weights.zip' (139Mo)
                self.agent.save(compute_name[:-4])

                #bucket_save("new_weights.zip")
                uploading = True
                blob = utils.interface_bucket(project, bucket, agent_name, compute_name)
                utils.upload_download(blob, agent_name, compute_name, uploading)

                #Evaluate
                score = self.evaluate()

                with open('reward.txt','a') as file:
                    file.write(f"{i} \t {self.n_steps} \t {score}\n")

                i += 1
                print(f'{i}# : Server')


# CLIENT
class Client(Agent):

    def __init__(self,  environement):
        super().__init__(environement)

    def game (self):
        self.agent.learn(total_timesteps=CFG.n_steps)

    def write_buffer(self, file_name:str):
        to_buffer = utils.extract_buffer(self.agent)

        with open(file_name,'wb') as f :
            pickle.dump(to_buffer, f)

    def new_weights(self, file_path):
        self.agent = A2C.load(file_path)

    def run(self, project, bucket, agent_name, file_name, uploading, compute_name):

        i = 0
        while True:
            self.game()

            self.write_buffer(f'{agent_name+file_name}') # WIP : Variables

            blob = utils.interface_bucket(project, bucket, agent_name, file_name)
            utils.upload_download(blob, agent_name, file_name, uploading)

            while True:
                #time.sleep(client_wait_time)
                #init_timestamp, is_done = switch(self.init_timestamp)
                blob = utils.interface_bucket(project, bucket, agent_name, compute_name)

                try:
                    # is_done=switch(blob, self.init_timestamp)
                    blob_time = utils.get_timestamp(blob)
                except:
                    blob_time = 0

                if self.init_timestamp < blob_time:
                    #new_weights = bucket_load("new_weights.zip")
                    uploading = False
                    blob = utils.interface_bucket(project, bucket, agent_name, compute_name)
                    utils.upload_download(blob, agent_name, compute_name, uploading)

                    #self.new_weights(f"{new_weights[:-4]}")
                    # self.new_weights("new_weights")
                    print("weights loaded in client")
                    break

            i += 1
            print(f'{i}# : Client')
