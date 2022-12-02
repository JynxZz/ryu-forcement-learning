from stable_baselines3 import A2C
import datetime
import time
import pickle

from stable_baselines3.common.logger import configure

from scripts.config import CFG
import scripts.utils as utils

# AGENT
class Agent():

        def __init__(self, env):
            self.env = env
            self.agent = A2C("MultiInputPolicy", self.env , n_steps= CFG.buffer_size)

            self.init_timestamp = time.time()

# SERVER
class AgentServer(Agent):

    def __init__(self,  env):
        super().__init__(env)

    def run(self):

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
                blob = utils.get_blob(project, bucket, agent_name, compute_name)
                utils.upload_download(blob, agent_name, compute_name, uploading)

                #TODO : Code evaluate method
                #server.evaluate()

                break


# CLIENT
class AgentClient(Agent):

    def __init__(self,  environement, n_steps):
        super().__init__(environement, n_steps)

    def game (self):
        self.agent.learn(total_timesteps= self.n_steps)

    def write_buffer(self, file_name:str):
        to_buffer = utils.extract_buffer(self.agent)

        with open(file_name,'wb') as f :
            pickle.dump(to_buffer, f)

    def new_weights(self, file_path):
        self.agent = A2C.load(file_path)

    def run(self, project, bucket, agent_name, file_name, uploading, compute_name):
        while True:
            self.game()

            self.write_buffer(f'{agent_name+file_name}') # WIP : Variables

            blob = utils.get_blob(project, bucket, agent_name, file_name)
            utils.upload_download(blob, agent_name, file_name, uploading)

            while True:
                #time.sleep(client_wait_time)
                #init_timestamp, is_done = switch(self.init_timestamp)
                blob = utils.get_blob(project, bucket, agent_name, compute_name)

                try:
                    # is_done=switch(blob, self.init_timestamp)
                    blob_time = utils.get_timestamp(blob)
                except:
                    blob_time = 0

                if self.init_timestamp < blob_time:
                    #new_weights = bucket_load("new_weights.zip")
                    uploading = False
                    blob = utils.get_blob(project, bucket, agent_name, compute_name)
                    utils.upload_download(blob, agent_name, compute_name, uploading)

                    #self.new_weights(f"{new_weights[:-4]}")
                    # self.new_weights("new_weights")
                    print("weights loaded in client")
                    break

            break
