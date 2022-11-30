from stable_baselines3 import PPO, A2C

from time import sleep
from scripts.utils import *


# variables
server_wait_time = 30
client_wait_time = 10
client_done = False
server_done = False

n_steps = 10


class Agent():


    def __init__(self, agent, env, is_serv = True):
        self.agent = agent
        self.env = env
        self.is_serv = is_serv

    def run(self, is_serv= True):
        if is_serv:
            pass
        else:
            pass



# SERVER

class AgentServer():
    init_timestamp = datetime.now()

    def __init__(self,  environement, n_steps):
        self.env = environement
        self.n_steps = n_steps
        self.agent = A2C("MultiInputPolicy", self.env , n_steps= self.n_steps)

    def compute(self, file_path, file_name):
        with open(file_path, 'rb') as f:
            imported_obs = pickle.load(f)

        #Importing buffer
        self.agent = import_buffer(imported_obs,self.agent) # TODO: no return inside method

        #Server Agent Training
        self.agent.train()

        #Saving parameters in 'weights.zip' (139Mo)
        self.agent.save(file_name)


    # def run(self):
    #     while True:
    #         sleep(server_wait_time)

    #         if client_done:
    #             data = local_read()

    #             new_weights = data + "new weights" # Concat & Compute weights

    #             local_save(new_weights)
    #             print('Send new weights')
    #             server_done = True
    #             client_done = False



# CLIENT

class AgentClient():
    init_timestamp = datetime.now()

    def __init__(self,  environement, n_steps):
        self.env = environement
        self.n_steps = n_steps
        self.agent = A2C("MultiInputPolicy", self.env , n_steps= self.n_steps)


    def game (self):
        self.agent.learn(total_timesteps= self.n_steps)

    def write_buffer(self, file_name:str):
        to_buffer = extract_buffer(self.agent)

        with open(file_name,'wb') as f :
            pickle.dump(to_buffer, f)

    def new_weights(self, file_path):
        self.agent = A2C.load(file_path)


    # def run(self):
    #     while True:
    #         # self.agent.get_obs(1_000) # play
    #         # data = self.agent.buffer() #
    #         data = str(i)

    #         local_save(data)
    #         client_done = True
    #         print("Save Own Obs")
    #         while True:
    #             sleep(client_wait_time)
    #             if server_done:

    #                 new_weights = local_read()
    #                 self.agent.comute(new_weights)
    #                 server_done = False



if __name__ == '__main__':
    env = ...
    n_steps = ...
    client = AgentClient(env, n_steps)
    server = AgentServer(env, n_steps)
