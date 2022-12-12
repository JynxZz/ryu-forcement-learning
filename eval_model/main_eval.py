import diambra
import diambra.arena
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env

import eval_agent

from config_eval import CFG

import argparse

"""
This is a Python script which uses the diambra library to evaluate an agent using the stable baselines3 library.
The script uses an argument parser to take two arguments and an object of the Config_eval class to initialize the evaluation process.
It then creates an instance of the EvalAgent() class and calls the iter_evaluate() method to evaluate the agent.

Parameters
----------
A list containing two arguments which are used to initialize the evaluation process :
        name of the agent : str
        weights use for the eval : str

Returns
----------
Nothing is returned from this script.
"""

parser = argparse.ArgumentParser()
parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)

args = parser.parse_args()


CFG.init(args.list[0], args.list[1])

eval_agent = eval_agent.EvalAgent()

eval_agent.iter_evaluate(CFG.name, CFG.eval_iter)
eval_agent.upload_eval(CFG.name)
