from stable_baselines3 import A2C
from scripts.utils import *
import datetime
from time import sleep
from scripts.config import *


# AGENT
class Agent():
        def __init__(self,  environement, n_steps):
            self.env = environement
            self.n_steps = n_steps
            self.agent = A2C("MultiInputPolicy", self.env , n_steps= self.n_steps)


# SERVER
class AgentServer(Agent):
    init_timestamp = datetime.datetime.now()

    def __init__(self,  environement, n_steps):
        super().__init__(environement, n_steps)

    def compute(self, file_path, file_name):
        with open(file_path, 'rb') as f:
            imported_obs = pickle.load(f)

        #Importing buffer
        self.agent.rollout_buffer = import_buffer(imported_obs, self.agent) # TODO: no return inside method

        #Server Agent Training
        self.agent.train()

        #Saving parameters in 'weights.zip' (139Mo)
        self.agent.save(file_name)

    def run(self):
        while True:
            sleep(server_wait_time)
            #init_timestamp, is_done = switch(self.init_timestamp)
            is_done=True

            if is_done:
                #buffer_1 = bucket_load("agent_one_obs.pickle")
                # buffer_2 = bucket_load("agent_two_obs.pickle")
                # buffer_3 = bucket_load("agent_three_obs.pickle")

                # TODO : Concat when more than 1 client
                # concat_buffer()

                self.compute("agent_one_obs.pickle", "new_weights")

                #bucket_save("new_weights.zip")

                #TODO : Code evaluate method
                #server.evaluate()

                break


# CLIENT
class AgentClient(Agent):
    init_timestamp = datetime.datetime.now()

    def __init__(self,  environement, n_steps):
        super().__init__(environement, n_steps)

    def game (self):
        self.agent.learn(total_timesteps= self.n_steps)

    def write_buffer(self, file_name:str):
        to_buffer = extract_buffer(self.agent)

        with open(file_name,'wb') as f :
            pickle.dump(to_buffer, f)

    def new_weights(self, file_path):
        self.agent = A2C.load(file_path)

    def run(self):
        while True:
            #self.game()

            #self.write_buffer("agent_one_obs.pickle") # WIP : Variables

            #bucket_save("agent_one_obs.pickle")


            while True:
                #sleep(client_wait_time)
                #init_timestamp, is_done = switch(self.init_timestamp)
                is_done=True

                if is_done:
                    #new_weights = bucket_load("new_weights.zip")

                    #self.new_weights(f"{new_weights[:-4]}")
                    self.new_weights("new_weights")
                    print("weights loaded in client")
                    break

            break
