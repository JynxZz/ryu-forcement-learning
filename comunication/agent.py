from time import sleep
from scripts.utils import local_save, load_weights, load_new_weight, bucket_save

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
            while True:
                sleep(server_wait_time)

                if client_done:
                    data = load_weights()
                    new_weights = self.train(data)

                    bucket_save(data)

        else:
            while True:
                self.agent.get_obs(1_000)
                data = self.agent.buffer()

                bucket_save(data)

                while True:
                    sleep(client_wait_time)

                    if server_done:
                        load_new_weight()
                        break


if __name__ == '__main__':
    agent = Agent('agent', 'env', True)
    agent.run()
