import json
import random
import numpy as np
import random 

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
        print("Cosine Similarity Score between '{}' and '{}': {:.4f}".format(word1, word2, similarity_score))
        return similarity_score
    else:
        print("One or both words not found in the GloVe vectors.")
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

def information_guess(words, goal, attr):
    guess = None
    best_weight = float('inf')  # Initialize to positive infinity for MSE
    for word in words:
        word_attr = [value for key, value in attr[words.index(word)].items() if isinstance(value, (int, float))]
        goal_attr = [value for key, value in attr[words.index(goal)].items() if isinstance(value, (int, float))]

        mse = calculate_mse(word_attr, goal_attr)  # Calculate Mean Squared Error
        if mse < best_weight:
            best_weight = mse
            guess = word
            if random.random() < 0.80:
                return guess
    return guess

def calculate_mse(word_attr, goal_attr):
    
    squared_diffs = [(a - b) ** 2 for a, b in zip(word_attr, goal_attr)]
    mse = np.mean(squared_diffs)
    
    return mse


def intersection(list1, list2):
    list3 = [v for v in list1 if v in list2]
    return list3

def eliminate(words, attr, goal, guess, time):
    # if guess word is same as goal word, found it
    time += 1
    print("Guessing", guess, "\n")
    if goal == guess:
        return guess, time
    # otherwise start eliminating
    guess_attr = attr[words.index(guess)]
    goal_attr = attr[words.index(goal)]
    compared = []
    # compare guess word with goal word and make list of whether each attribute is correct or not
    for x in goal_attr:
        # if attribute is number, see if goal attribute is bigger or smaller
        if isinstance(goal_attr[x], float) or isinstance(goal_attr[x], int):
            if goal_attr[x] > guess_attr[x]:
                compared.append(">")
            elif goal_attr[x] < guess_attr[x]:
                compared.append("<")
            else:
                compared.append(True)
        elif isinstance(goal_attr[x], list):
            if not intersection(goal_attr[x], guess_attr[x]):
                compared.append(False)
            else:
                compared.append(intersection(goal_attr[x], guess_attr[x]))
        # else check if attributes are the same or not
        else:
            if goal_attr[x] == guess_attr[x]:
                compared.append(True)
            else:
                compared.append(False)
    new_words = words.copy()
    new_attr = attr.copy()
    index = -1
    # run through all words/items in list and remove any that don't match the new criteria
    for x in attr:
        index += 1
        for i in range(len(compared) - 1):
            if (x not in new_attr):
                break
            elif isinstance(compared[i], str):
                # if goal > guess, remove any words/items that are smaller or same
                if compared[i] == ">":
                    if list(x.values())[i] <= list(guess_attr.values())[i]:
                        print(words[index], "eliminated")
                        new_words.remove(words[index])
                        new_attr.remove(x)
                        break
                # if goal < guess, remove any words/items that are bigger or same
                else:
                    if list(x.values())[i] >= list(guess_attr.values())[i]:
                        print(words[index], "eliminated")
                        new_words.remove(words[index])
                        new_attr.remove(x)
                        break      
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    if len(new_words) != len(words):
        print("\nWords Left:", new_words, "\n")
    return eliminate(new_words, new_attr, goal, information_guess(new_words, goal, new_attr), time)

def human_evaluate(og_words, words, og_attr, attr, goal, time, usingNLP = False, word_vectors = None):
    # if guess word is same as goal word, found it
    guess = ""
    while guess not in og_words:
        if time > 0:
            guess = input("\nGuess a new word: ")
        else:
            guess = input("\n")
        if guess not in og_words:
            print("Please try again, remember to use capitals and punctuation if needed...")
    # otherwise start eliminating
    time += 1
    guess_attr = og_attr[og_words.index(guess)]
    goal_attr = og_attr[og_words.index(goal)]
    compared = []
    # compare guess word with goal word and make list of whether each attribute is correct or not
    for x in goal_attr:
        # if attribute is number, see if goal attribute is bigger or smaller
        if isinstance(goal_attr[x], float) or isinstance(goal_attr[x], int):
            if goal_attr[x] > guess_attr[x]:
                compared.append(">")
            elif goal_attr[x] < guess_attr[x]:
                compared.append("<")
            else:
                compared.append(True)
        elif isinstance(goal_attr[x], list):
            if not intersection(goal_attr[x], guess_attr[x]):
                compared.append(False)
            else:
                compared.append(intersection(goal_attr[x], guess_attr[x]))
        # else check if attributes are the same or not
        else:
            if goal_attr[x] == guess_attr[x]:
                compared.append(True)
            else:
                compared.append(False)
    #print(guess, compared)
    result = dict()
    for i in range(len(compared)):
        if isinstance(compared[i], bool):
            if compared[i] == True:
                result[list(og_attr[og_words.index(guess)].keys())[i]] = "Correct"
            elif compared[i] == False:
                result[list(og_attr[og_words.index(guess)].keys())[i]] = "Incorrect"
        elif isinstance(compared[i], list):
            if not compared[i]:
                result[list(og_attr[og_words.index(guess)].keys())[i]] = "Incorrect"
            else:
                result[list(og_attr[og_words.index(guess)].keys())[i]] = compared[i]
        else:
            result[list(og_attr[og_words.index(guess)].keys())[i]] = compared[i]
    print("\n", result, "\n")
    if goal == guess:
        return guess, time

    if usingNLP:
        output_similarity(guess, goal, word_vectors)

    new_words = words.copy()
    new_attr = attr.copy()
    # run through all words/items in list and remove any that don't match the new criteria
    index = -1
    if guess in words:
        for x in attr:
            index += 1
            for i in range(len(compared)):
                if (x not in new_attr):
                    break
                elif isinstance(compared[i], str):
                    # if goal > guess, remove any words/items that are smaller or same
                    if compared[i] == ">":
                        if list(x.values())[i] <= list(guess_attr.values())[i]:
                            new_words.remove(words[index])
                            new_attr.remove(x)
                            break
                    # if goal < guess, remove any words/items that are bigger or same
                    else:
                        if list(x.values())[i] >= list(guess_attr.values())[i]:
                            new_words.remove(words[index])
                            new_attr.remove(x)
                            break
                elif isinstance(compared[i], list):
                    check = False
                    for l in compared[i]:
                        if l not in list(x.values())[i]:
                            new_words.remove(words[index])
                            new_attr.remove(x)
                            check = True
                            break
                    if check == True:
                        break
                # remove any words/items that dont have the same non-numbered attribute
                else:
                    if compared[i] == True:
                        if list(x.values())[i] != list(guess_attr.values())[i]:
                            new_words.remove(words[index])
                            new_attr.remove(x)
                            break
                    else:
                        if list(x.values())[i] == list(guess_attr.values())[i]:
                            new_words.remove(words[index])
                            new_attr.remove(x)
                            break
    see_list = input("Would you like to see the new list? [Y/N]: ")
    if see_list == "Y" or see_list == "y":
        print("\n", new_words, "\n")
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    return human_evaluate(og_words, new_words, og_attr, new_attr, goal, time, usingNLP, word_vectors)

def main(word_vectors, data, usingNLP, goal_word):
    # words is word bank in list form, attr is list of their respective attributes
    # words and attr share the same index
    words, attr = create_dicts(data)

    # choose goal word by randomly selecting word/item from word bank
    time = 0
    goalword = goal_word
    guess = rng_guess(words)
    final, time = eliminate(words, attr, goalword, guess, time)
    print("Found Goal Word:", final)
    print("Number of Guesses:", time)

    # while True:
    #     try:
    #         input1 = int(input("Enter 1 for bot\nEnter 2 for human: "))
    #         break
    #     except:
    #         print("Please input 1 or 2...")
    # time = 0
    # if input1 == 1:
    #     print("\nGoal is", goalword, "\n")
    #     # guess = half_eliminate(words, attr) [EXAMPLE]
    #     guess = rng_guess(words)
    #     final, time = eliminate(words, attr, goalword, guess, time)
    #     print("Found Goal Word:", final)
    #     print("Number of Guesses:", time)
    #     input2 = input("\nPlay Again? [Y/N]: ")
    #     if input2 == "Y" or input2 == "y":
    #         main(word_vectors, data, usingNLP)
    #     return
    # elif input1 == 2:
    #     print("\nGuess a word from the following list:")
    #     print(words)
    #     final, time = human_evaluate(words, words, attr, attr, goalword, time, usingNLP, word_vectors)
    #     print("Congrats, the goal word is:", final)
    #     print("Number of Guesses:", time)
    #     input2 = input("\nPlay Again? [Y/N]: ")
    #     if input2 == "Y" or input2 == "y":
    #         main(word_vectors, data, usingNLP)
    #     return
    # else:
    #     print("Please input 1 or 2...")
    #     main(word_vectors, data, usingNLP)
    #     return
    
def run(json, goal_word):
    usingNLP = False
    word_vectors = None
    # snli_jsonl_path = "./snli_1.0/snli_1.0_train.jsonl"  # Adjust this path to your SNLI JSONL file location
    # glove_model_path = "./glove.6B/glove.6B.300d.txt"  # Adjust this path to your GloVe file location
    
    # snli_data = load_jsonl(snli_jsonl_path)
    # word_vectors = load_glove_vectors(glove_model_path)

    
    main(word_vectors, json, usingNLP, goal_word)