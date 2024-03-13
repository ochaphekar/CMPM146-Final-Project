

import numpy as np

"""
Here is where you will implement your functions for state-based conditional checks. As with 
actions, each function should only take the target word and json file. 
"""

# conditional check 1
# Check: Check the index of the guess and the actual word and rarrow down the list of potential guesses to a new list of words that only contains words of that given index. 
"""
Function filter_words_by_index(words, guessed_index, guess_accuracy):
    filtered_words = empty list
    
    For each word in words:
        if guess_accuracy == -1 and if index of word less than equal to guessed_index:
            Add all words with lower index than guess to filtered words 
        elif guess_accuracy == 1 and if index of word greater than equal to guessed_index:
            Add all words with higher index than guess to filtered words.
        elif guess_accuracy == 0 and if index of word equals guessed_index:
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
## Narrow down the list of words to a list of words form the JSON that only contains the same number of parts of speech as the actual word. 

"""
Function filter_words_by_part_of_speech(words, target_parts_of_speech): #ask about this what info do we get
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

# conditional check 4
# Check for vowel count: create a new filtered list of words that only match the vowel count of the actual word.
"""""
Function filter_words_by_vowel_count(words, guessed_vowel_count, guess_accuracy):
    filtered_words = empty list
    
    For each word in words:
        if guess_accuracy == -1 and if vowel count of word less than equal to guessed_vowel_count:
            Add all words with lower vowel count than guess to filtered words
        elif guess_accuracy == 1 and if vowel count of word greater than equal to guessed_vowel_count:
            Add all words with higher vowel count than guess to filtered words.
        elif guess_accuracy == 0 and if vowel count of word equals guessed_vowel_count:
            Add word to filtered_words
    
    Return filtered_words
"""
# conditional check 5
#Check for length count: FILTER out words that don't have the same length count. 
"""
Function filter_words_by_length(words, guessed_length, guess_accuracy):
    filtered_words = empty list
    
    For each word in words:
        if guess_accuracy == -1 and if length of word less than equal to guessed_length:
            Add all words with lower length than guess to filtered words
        elif guess_accuracy == 1 and if length of word greater than equal to guessed_length:
            Add all words with higher length than guess to filtered words.
        elif guess_accuracy == 0 and if length of word equals guessed_length:
            Add word to filtered_words
    Return filtered_words
"""
