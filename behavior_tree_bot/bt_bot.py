#!/usr/bin/env python
#

"""
// This is where you impement your overall strategy to play the game. 
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check
import json
import random

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # The start sequence will run the production bot to take over the cloest
    # planets from its starting planet. The production bot's
    # strategy fits our needs for this. This will only run until a certain
    # number of planets have been taken over. 
    numerical_strategy = Sequence(name="Numerical Strategy")
    numerical_check = Check(check_numerical_attributes)
    numerical_action = Action(htn_information)
    numerical_strategy.child_nodes = [numerical_check, numerical_action]

    greedy_strategy = Sequence(name="Greedy Strategy")
    greedy_check = Check(check_greedy_attributes)
    greedy_action = Action(greedy_information)
    greedy_strategy.child_nodes = [greedy_check, greedy_action]

    nlp_strategy = Sequence(name="Nlp Strategy")
    nlp_check = Check(check_nlp_attributes)
    nlp_action = Action(nlp_information)
    nlp_strategy.child_nodes = [nlp_check, nlp_action]

    root.child_nodes = [numerical_strategy, greedy_strategy, nlp_strategy]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(json, word):
    behavior_tree.execute(json, word)

if __name__ == '__main__':
    # logging
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
    
    # get json file
    words_filename = 'pokemon.json'
    with open(words_filename) as f:
        data = json.load(f)

    # choose goal word by randomly selecting word/item from word bank
    goalword = random.choice(list(data.keys()))
    print("Goal is", goalword)

    behavior_tree = setup_behavior_tree()
    do_turn(data, goalword)


