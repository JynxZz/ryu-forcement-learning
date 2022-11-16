import matplotlib.pyplot as plt
import seaborn as sns

from IPython import display

plt.ion()

def plot(time, reward):

    display.clear_output(wait=True)
    display.display(plt.gcf())

    plt.clf()
    plt.title('Training...')
    plt.xlabel('Time')
    plt.ylabel('Reward')
    plt.plot(time)
    plt.plot(reward)
    plt.ylim(ymin=0)
    # plt.text(len(time)-1, time[-1], str(time[-1]))
    # plt.text(len(reward)-1, reward[-1], str(reward[-1]))
    plt.show(block=False)
    plt.pause(.1)
