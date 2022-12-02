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
                buffer_ryu = utils.download(blob, CFG.path_ryu)
                # buffer_ken = bucket_load("agent_two_obs.pickle")
                # buffer_osu = bucket_load("agent_three_obs.pickle")

                # TODO : Deuxième fonction, prepare buffers

                # 2.1. Load files from pickles
                with open(CFG.obs_ryu, 'rb') as f:
                    obs_ryu = pickle.load(f)

                # TODO : Concat when more than 1 client
                # 2.2. Concat pickles
                # concat_obs = concat_buffer([obs_ryu, obs_ken, obs_osu])

                # 2.3. Load the concat buffer
                self.agent.rollout_buffer = utils.load_buffer(obs_ryu, self.agent) # TODO: no return inside method

                # 2.4. Prep buffer logging
                logg = configure(folder='/tmp/')
                self.agent.set_logger(logg)

                # Step 3 - Compûte weights
                self.agent.train()

                #Saving parameters in 'weights.zip' (139Mo)
                self.agent.save(CFG.weights[:-4])

                blob = utils.get_blob_server()
                utils.upload(blob, CFG.weights)

                #TODO : Code evaluate method
                #server.evaluate()

                break


# CLIENT
class AgentClient(Agent):

    def __init__(self,  env):
        super().__init__(env)

    def game (self):
        self.agent.learn(total_timesteps= CFG.buffer_size)

    def write_buffer(self):
        to_buffer = utils.extract_buffer(self.agent)

        with open(f'{CFG.name+CFG.obs}','wb') as f :
            pickle.dump(to_buffer, f)

    def new_weights(self):
        self.agent = A2C.load(CFG.obs)

    def run(self):
        while True:
            self.game()

            self.write_buffer()

            blob = utils.get_blob_client()
            utils.upload(blob, f'{CFG.name+CFG.obs}')

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

            break
