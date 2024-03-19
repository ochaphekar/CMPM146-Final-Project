import sys
import random
sys.path.insert(0, '../')
import HTN_information
import HTN_greedy
import HTN_NLP

#dictionary behaviors

#greedy behavior - looks for basically getting really lucky w/ the palindrome or index to massively cut search space early
def greedy_information(json, word):
    HTN_greedy.run(json, word)

#information behavior - looks more for parts of speech, vowel count, and length to cut search space consistently
def htn_information(json, word):
    HTN_information.run(json, word)

#contexto behavior 
def nlp_information(json, word):
    HTN_NLP.run(json, word)
