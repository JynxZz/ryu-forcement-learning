from time import sleep
from scripts.utils import local_save, local_read, is_done, load_weights, load_new_weight, bucket_save

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
                print("coucou")

                if client_done:
                    data = load_weights()
                    new_weights = self.train(data)
                    print("salut")
                    bucket_save(new_weights)

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


# SERVER

class Server():
    def __init__(self, agent, environement):
        self.agent = agent
        self.env = environement

    def run(self):
        while True:
            sleep(server_wait_time)
            print('Waiting weight')

            if client_done:
                data = local_read()

                new_weights = data + "new weights"

                local_save(new_weights)
                print('Send new weights')

# CLIENT

class Client():
    i = 0
    def __init__(self, agent, environement):
        self.agent = agent
        self.env = environement

    def run(self):
        while True:
            # self.agent.get_obs(1_000)
            # data = self.agent.buffer()
            i += 1
            if i == 100:
                data = i
                local_save(data)

            if server_done:
                data = local_read()

                new_weights = data + "new weights"

                local_save(new_weights)
                print('Send new weights')


if __name__ == '__main__':
    agent = Agent('agent', 'env', True)
    agent.run()
