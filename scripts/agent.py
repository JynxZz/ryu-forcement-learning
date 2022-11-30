from stable_baselines3 import A2C
from scripts.utils import *


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
