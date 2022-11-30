from time import sleep
from scripts.utils import creation_date, local_save, local_read, is_done, load_weights, load_new_weight, bucket_save

# variables
server_wait_time = 30
client_wait_time = 10
client_done = False
server_done = False


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

class Server():
    def __init__(self, agent, environement):
        self.env = environement
        self.agent = agent

    def run(self):
        while True:
            sleep(server_wait_time)

            if client_done:
                data = local_read()

                new_weights = data + "new weights" # Concat & Compute weights

                local_save(new_weights)
                print('Send new weights')
                server_done = True
                client_done = False



# CLIENT

class Client():
    i = 0
    def __init__(self, agent, environement):
        self.agent = agent
        self.env = environement

    def run(self):
        while True:
            # self.agent.get_obs(1_000) # play
            # data = self.agent.buffer() #
            i += 1
            if i == 100:
            # if client_done:
                data = str(i)

                local_save(data)
                client_done = True
                print("Save Own Obs")
                while True:
                    sleep(client_wait_time)
                    if server_done:

                        new_weights = local_read()
                        self.agent.comute(new_weights)
                        server_done = False

old_timestamp= datetime.now()

while True:
    timestamp= creation_date()
    if old_timestamp < timestamp:
        old_timestamp = timestamp
        client_done = True
    
if __name__ == '__main__':
    pass
