import sys
sys.path.insert(0, '../')

#dictionary behaviors

#greedy behavior - looks for basically getting really lucky w/ the palindrome or index to massively cut search space early
"""
def greedy_behavior(words):
    if length 
    length_weight = [x1,x2,x3,x4,x5,x6,x7...];
    vowel_weight = [y1,y2,y3,y4,y5,y6,y7...];
    acceptable_weighted_value = z;
    
    words_to_guess_from = empty list;
    
    For each word in words:
        weighted_value = length_weight[word.length] + vowel_weight[word.vowel_count]
        if weighted_value > acceptable_weighted_value:
            words_to_guess_from.append(word)
            
    return random in words_to_guess_from;
"""




#information behavior - looks more for parts of speech, vowel count, and length to cut search space consistently
"""
def information_behavior(words):
    length.weight = x;
    vowel.weight = y;
    parts_of_speech.weight = z;
    max_weighted_value = 0
    best_word = None
    For each word in words:
        weighted_value = word.length*(length.weight) + word.vowel_count*(vowel.weight) + word.parts_of_speech*(parts_of_speech.weight)
        If weighted_value > max_weighted_value:
            max_weighted_value = weighted_value
            best_word = word
    
    return best_word

"""

#contexto behavior 
"""
assign a weight similar to greedy behavior for contexto
for example: if word is ranked 20,000 in the list, it has a 0.01 weight
if word is ranked 50 on thee list, it has a 10 weight

use this to prioritize contexto once a good contexto word is found


"""
#below is the code from p3?

"""
Here is where you will implement your functions for action nodes, typically issuing orders. 
Each function should only take the game state as a parameter. There are two actions already 
implemented here as examples: attack_weakest_enemy_planet and spread_to_weakest_neutral_planet.
"""

# attack node 1

# attack node 2

# attack node 3

# attack node 4