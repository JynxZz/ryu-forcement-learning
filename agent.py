from stable_baselines3 import PPO, A2C
import pickle
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env
from stable_baselines3.common.logger import configure
import numpy as np

"""
    Settings editable
"""

RATIO = 0
WIDTH = 384
HEIGHT = 224

settings = {
    'player': 'P1',
    'step_ratio': 6,
    'frame_shape': [WIDTH, HEIGHT, 0],
    'continue_game': 0.0,
    'show_final': False,
    'hardcore': False,
    'difficulty': 8,
    'characters': [["Chun-Li"], ["Random"]],
    'action_space': 'multi_discrete',
    'attack_but_combination': True,
}
wrappers_settings={}
wrappers_settings["reward_normalization"] = True
wrappers_settings["flatten"] = True

n_steps = 10

def extract_buffer(client_agent):
    #Extracting buffer
    buffer = client_agent.rollout_buffer
    observation = buffer.observations
    action = buffer.actions
    reward = buffer.rewards
    episode_start = buffer.episode_starts
    value = buffer.values
    log_prob = buffer.log_probs

    to_buffer = (observation, action,
                 reward, episode_start,
                 value, log_prob,
                 buffer.returns, buffer.advantages)
    return to_buffer

def add(buffers):
    #Stack buffers
    assert len(buffers)>2, "No buffer to add"
    n=len(buffers)
    init = buffers[0]
    a, b, c, d, e, f, g, h = init
    # a = init[0]
    # b = init[1]
    # c = init[2]
    # d = init[3]
    # e = init[4]
    # f = init[5]
    # g = init[6]
    # h = init[7]
    #print(np.vstack([b,buffers[1][1]]))
    for j in range(n-1):
        b = np.vstack([b,buffers[j+1][1]])
        c = np.vstack([c,buffers[j+1][2]])
        d = np.vstack([d,buffers[j+1][3]])
        e = np.vstack([e,buffers[j+1][4]])
        f = np.vstack([f,buffers[j+1][5]])
        g = np.vstack([g,buffers[j+1][6]])
        h = np.vstack([h,buffers[j+1][7]])

        for key in init[0].keys():
            a[key]=np.vstack([a[key],buffers[j+1][0][key]])

    return (a,b,c,d,e,f,g,h)

def import_buffer(imported_obs, server_agent):

    server_agent.rollout_buffer.reset()
    server_agent.rollout_buffer.buffer_size = server_agent.n_steps
    server_agent.rollout_buffer.observations = imported_obs[0]
    server_agent.rollout_buffer.actions = imported_obs[1]
    server_agent.rollout_buffer.rewards = imported_obs[2]
    server_agent.rollout_buffer.episode_starts = imported_obs[3]
    server_agent.rollout_buffer.values = imported_obs[4]
    server_agent.rollout_buffer.log_probs = imported_obs[5]
    server_agent.rollout_buffer.returns = imported_obs[6]
    server_agent.rollout_buffer.advantages = imported_obs[7]
    server_agent.rollout_buffer.generator_ready = True
    server_agent.rollout_buffer.pos=len(imported_obs[5])
    server_agent.rollout_buffer.full=True
    # logg = configure(folder='/tmp/')
    # server_agent.set_logger(logg)

    return server_agent

if __name__ == "__main__":

##Client Side##
    # Creation of environment from diambra
    env, _ = make_sb3_env("sfiii3n", settings, wrappers_settings)

    #Instancing Agent Agent("Policy", environment, n_steps)
    client_agent = A2C("MultiInputPolicy", env , n_steps=n_steps)
    #Total_timesteps(<= n_steps so it doesn't learn)
    client_agent.learn(total_timesteps= n_steps)
    #Saving parameters in 'weights.zip' (139Mo)
    # client_agent.save("weights")

    #Exporting buffer
    to_buffer = extract_buffer(client_agent)

    with open('to_buffer.pickle','wb') as f :
        pickle.dump(to_buffer, f)

    #Loading an agent from imported parameters (here in '/weights.zip')
    new_agent = A2C.load('weights')


##Server Side##

    # Creation of environment from diambra
    env, _ = make_sb3_env("sfiii3n", settings, wrappers_settings)

    #Import from bucket .pickle file
    with open('to_buffer.pickle', 'rb') as f:
        imported_obs = pickle.load(f)

    #Stacking observations

    #Training server agent from client agent's buffer
    server_agent = A2C("MultiInputPolicy", env, n_steps=n_steps)

    #Importing buffer
    server_agent=import_buffer(imported_obs,server_agent)

    #Server Agent Training
    server_agent.train()

    #Saving parameters in 'weights.zip' (139Mo)
    server_agent.save("weights")

    exit()
