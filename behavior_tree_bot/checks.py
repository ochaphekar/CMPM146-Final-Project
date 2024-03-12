
import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the target word and json file. 
"""

# conditional check 1
# Check: CHeck the index of the guess and the actual word and rarrow down the list of potential guesses to a new list of words that only contains words of that given index. 
"""
Function filter_words_by_index(words, target_index):
    filtered_words = empty list
    
    For each word in words:
        If index of word equals target_index:
            Add word to filtered_words
    
    Return filtered_words
"""



# conditional check 2
#Check: Check if both words are palindromes and create new list filtering out words that aren't palindromes
"""
Function filter_palindromes(words):
    filtered_words = empty list
    
    For each word in words:
        If word is a palindrome:
            Add word to filtered_words
    
    Return filtered_words
"""


# conditional check 3
# Check: The number of parts of speech the guess has compared to the actual word
- Narrow down the list of words to a list of words form the JSON that only contains the same number of parts of speech as the actual word. 

"""
Function filter_words_by_part_of_speech(words, target_parts_of_speech):
    filtered_words = empty list
    
    actual_word_parts_of_speech_count = count_parts_of_speech(actual_word)
    
    For each word in words:
        has_target_part_of_speech = False
        word_parts_of_speech_count = count_parts_of_speech(word)
        
        If word_parts_of_speech_count equals actual_word_parts_of_speech_count:
            For each part_of_speech in word's part_of_speech list:
                If part_of_speech is in target_parts_of_speech:
                    Set has_target_part_of_speech to True
                    Break out of the loop
            
            If has_target_part_of_speech is True:
                Add word to filtered_words
    
    Return filtered_words
    """

#conditional check 4
# contains one or more of the same parts of speech as the actual word. 

# conditional check 5
# Check for vowel count of guess vs. actual word

"""""
#Function filter_words_by_vowel_count(words, target_vowel_count):
    filtered_words = empty list
    
    For each word in words:
        vowel_count = 0
        For each letter in word:
            If letter is a vowel:
                Increment vowel_count
        
        If vowel_count equals target_vowel_count:
            Add word to filtered_words
    
    Return filtered_words
"""
# conditional check 5
#Check for length count: FILTER out words that don't have the same length count. 
"""
Function filter_words_by_length(words, target_length):
    filtered_words = empty list
    
    For each word in words:
        If length of word equals target_length:
            Add word to filtered_words
    
    Return filtered_words
"""
