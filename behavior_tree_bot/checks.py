

import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the target word and json file. 
"""


# conditional check 1
# Check: Check if word has at least 75% numerical attributes
def check_numerical_attributes(json_obj, word):
    if word not in json_obj:
        return False
    
    attr_count = 0
    total_attrs = len(json_obj[word])
    
    for attr in json_obj[word]:
        if isinstance(attr, int) or isinstance(attr, float):
            attr_count += 1
    
    return attr_count >= 0.75 * total_attrs


# conditional check 2
# Check: Check if word length is within average legnth of json words
def check_word_length(json_obj, word):
    if word not in json_obj:
        return False

    word_length = len(word)
    word_lengths = [len(w) for w in json_obj.keys()]
    
    q1 = np.percentile(word_lengths, 25)
    q3 = np.percentile(word_lengths, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return lower_bound <= word_length <= upper_bound


# conditional check 3
# Check: Check if word has at least 75% numerical attributes
def check_other_attributes(json_obj, word):
    if word not in json_obj:
        return False
    
    attr_count = 0
    total_attrs = len(json_obj[word])
    
    for attr in json_obj[word]:
        if (not isinstance(attr, int)) and (not isinstance(attr, float)):
            attr_count += 1
    
    return attr_count >= 0.60 * total_attrs

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
