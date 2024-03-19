

import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the target word and json file. 
"""


# conditional check 1
# Check: Check if word has at least 30% numerical attributes
def check_numerical_attributes(json_obj, word):
    if word not in json_obj:
        return False
    
    attr_count = 0
    total_attrs = len(json_obj[word])
    attr = json_obj[word]
    for key, value in attr.items():
        if isinstance(value, int) or isinstance(value, float):
            attr_count += 1
    
    return attr_count > (0.3 * total_attrs)


# conditional check 2
# Check: Check if word length is within average legnth of json words
def check_greedy_attributes(json_obj, word):
    if word not in json_obj:
        return False

    word_length = len(word)
    word_lengths = [len(w) for w in json_obj.keys()]
    
    mean_length = np.mean(word_lengths)
    std_length = np.std(word_lengths)

    lower_bound = mean_length - std_length
    upper_bound = mean_length + std_length

    return lower_bound <= word_length <= upper_bound

# conditional check 3
# Check: Check if word has at least 70% non-numerical attributes
def check_nlp_attributes(json_obj, word):
    if word not in json_obj:
        return False
    
    attr_count = 0
    total_attrs = len(json_obj[word])
    attr = json_obj[word]
    for key, value in attr.items():
        if isinstance(value, int) or isinstance(value, float):
            attr_count += 1
    
    return attr_count < (0.3 * total_attrs)

