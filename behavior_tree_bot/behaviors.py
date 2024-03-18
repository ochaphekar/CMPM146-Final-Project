import sys
import random
sys.path.insert(0, '../')
import HTN_information

#dictionary behaviors

#greedy behavior - looks for basically getting really lucky w/ the palindrome or index to massively cut search space early

def greedy_behavior(words):
    index_weight = [2, 8, 7, 13, 15, 9, 18, 11, 4, 22, 23, 16, 12, 17, 3, 10, 24, 14, 5, 1, 20, 19, 6, 26, 21, 25] #a-z
    length_weight = [15, 14, 12, 11, 9, 7, 5, 3, 1, 2, 4, 6, 8, 10, 13] #1-15 letters
    a_weight = [1, 2, 3, 4, 5, 6, 7] #0-6 a's
    #a_weight = [y1,y2,y3,y4,y5,y6,y7] 
    e_weight = [1, 2, 3, 4, 5, 6, 7] #0-6 e's
    #e_weight = [y1,y2,y3,y4,y5,y6,y7] 
    i_weight = [1, 2, 3, 4, 5, 6, 7] #0-6 i's
    #i_weight = [y1,y2,y3,y4,y5,y6,y7] 
    o_weight = [1, 2, 3, 4, 5, 6, 7] #0-6 o's
    #o_weight = [y1,y2,y3,y4,y5,y6,y7] 
    u_weight = [1, 2, 3, 4, 5, 6, 7] #0-6 u's
    #u_weight = [y1,y2,y3,y4,y5,y6,y7] 
    acceptable_weighted_value = 30
    
    words_to_guess_from = []
    best_word = None
    best_value = 0
    
    for word in words:
        weighted_value = length_weight[word["length"] - 1] + a_weight[word["contains_a"] - 1] + e_weight[word["contains_e"] - 1] + i_weight[word["contains_i"] - 1] + o_weight[word["contains_o"] - 1] + u_weight[word["contains_u"] - 1] + index_weight[word["index"] - 1]
        if weighted_value > best_value:
            best_value = weighted_value
            best_word = word
        if weighted_value >= acceptable_weighted_value:
            words_to_guess_from.append(word)
    
    if words_to_guess_from == []:
        return best_word
    return random.choice(words_to_guess_from)




#information behavior - looks more for parts of speech, vowel count, and length to cut search space consistently
def htn_information(json, word):
    HTN_information.run(json, word)

#contexto behavior 

