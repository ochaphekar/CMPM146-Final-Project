import json
import random
import numpy as np

## NLP functions

# Load SNLI Corpus
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Load GloVe word vectors
def load_glove_vectors(file_path):
    word_vectors = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype=np.float64)  # Use np.float64 instead of np.float
            word_vectors[word] = vector
    return word_vectors

# Calculate cosine similarity between two word vectors
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)
    return similarity

def output_similarity(word1, word2, word_vectors):
    # Check if the words exist in the GloVe vectors
    if word1 in word_vectors and word2 in word_vectors:
        vector1 = word_vectors[word1]
        vector2 = word_vectors[word2]

        # Calculate cosine similarity between the two word vectors
        similarity_score = cosine_similarity(vector1, vector2)
        # print("Cosine Similarity Score': {:.4f}".format(similarity_score))
        return similarity_score
    else:
        return 0.0001
        return None

## End of NLP functions

# use json data to separate each word/item into lists
def create_dicts(data):
    # declare lists for both the words and their attributes
    wordlist = []
    attrlist = []

    # add to both lists the word and their attributes respectively
    for x in data.keys():
        wordlist.append(x)
        attrlist.append(data[x])

    return wordlist, attrlist

# guess a random word/item from current list of possible choices
def rng_guess(words):
    guess = random.choice(words)
    return guess

def intersection(list1, list2):
    list3 = [v for v in list1 if v in list2]
    return list3

def NLP_eliminate(words, goal, guess, time, word_vectors):
    # if guess word is same as goal word, found it
    time += 1
    print("Guessing", guess, "\n")
    if goal == guess:
        return guess, time
    # otherwise start eliminating

    # NLP score of the guess word
    guess_NLP = output_similarity(guess, goal, word_vectors)

    # Eliminate words that have a lower NLP score than the guess word
    for word in words:
        if output_similarity(word, goal, word_vectors) < guess_NLP:
            print(word, "eliminated")
            words.remove(word)

    new_words = words.copy()
    
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    if len(new_words) != len(words):
        print("\nWords Left:", new_words, "\n")
    return NLP_eliminate(new_words, goal, rng_guess(new_words), time, word_vectors)

def main(word_vectors, data, goal_word):
    # words is word bank in list form, attr is list of their respective attributes
    # words and attr share the same index
    words = create_dicts(data)

    # sort words alphabetically
    words.sort()
    print("Word Bank:", words, "\n")

    # choose goal word by randomly selecting word/item from word bank
    goalword = random.choice(words)
    time = 0
    print("\nGoal is", goalword, "\n")
    # guess = half_eliminate(words, attr) [EXAMPLE]
    guess = rng_guess(words)
    final, time = NLP_eliminate(words, goalword, guess, time, word_vectors)
    print("Found Goal Word:", final)
    print("Number of Guesses:", time)
    
def run(json, goal_word):

    usingNLP = True
    snli_jsonl_path = "./snli_1.0/snli_1.0_train.jsonl"  # Adjust this path to your SNLI JSONL file location
    glove_model_path = "./glove.6B/glove.6B.300d.txt"  # Adjust this path to your GloVe file location
    
    snli_data = load_jsonl(snli_jsonl_path)
    word_vectors = load_glove_vectors(glove_model_path)

    main(word_vectors, json, goal_word)
