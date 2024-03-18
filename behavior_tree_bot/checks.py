

import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the target word and json file. 
"""


# conditional check 1
# Check: Check the index of the guess and the actual word and rarrow down the list of potential guesses to a new list of words that only contains words of that given index. 

def filter_words_by_num_attributes(words, guessed_attribute, attribute_type, guess_accuracy):
    filtered_words = []
    attributes = ["index", "contains_a", "contains_e", "contains_i", "contains_o", "contains_u", "length"] 
    #attribute_type is 0-6   ^
    #guess_accuracy is -1, 0, 1
    
    for word in words:
        if guess_accuracy == -1 and word[attributes[attribute_type]] < guessed_attribute:
            filtered_words.append(word)
        elif guess_accuracy == 1 and word[attributes[attribute_type]] > guessed_attribute:
            filtered_words.append(word)
        elif guess_accuracy == 0 and word[attributes[attribute_type]] == guessed_attribute:
            filtered_words.append(word)
    
    return filtered_words


# conditional check 2
#Check: Check if both words are palindromes and create new list filtering out words that aren't palindromes

def filter_by_palindromes(words, guessed_attribute, guess_accuracy):
    filtered_words = []
    
    for word in words:
        if guess_accuracy != 0 and word["is_palindrome"] != guessed_attribute:
            filtered_words.append(word)
        elif guess_accuracy == 0 and word["is_palindrome"] == guessed_attribute:
            filtered_words.append(word)            
    return filtered_words


# conditional check 3
# Check: The number of parts of speech the guess has compared to the actual word
## Narrow down the list of words to a list of words form the JSON that only contains the same number of parts of speech as the actual word. 


#Guess word: whatever
#Parts of speech ["noun", "verb", "adjective"]

#Actual word:whatever2
#Parts of speech ["noun", "adverb"]

#Response: false, ["noun"]

def filter_words_by_pos(words, guess_parts_of_speech, is_matching, matching_parts_of_speech):
    filtered_words = []
    wrong_pos = []
    if is_matching == False:
        wrong_pos = [x for x in guess_parts_of_speech if x not in matching_parts_of_speech]
    
    for word in words:
        if is_matching == True and word["part_of_speech"] == matching_parts_of_speech:
            filtered_words.append(word)
        elif is_matching == False:
            is_filtered = False
            for part_of_speech in wrong_pos:
                if part_of_speech in word["part_of_speech"]:
                    is_filtered = True
                    break
            for part_of_speech in matching_parts_of_speech:
                if part_of_speech not in word["part_of_speech"]:
                    is_filtered = True
                    break
            if is_filtered == False:
                filtered_words.append(word)
    return filtered_words
