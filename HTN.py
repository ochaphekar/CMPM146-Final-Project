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
    

def eliminate(words, attr, goal, guess, time):
    # if guess word is same as goal word, found it
    print("Guessing", guess)
    if goal == guess:
        return guess, time
    # otherwise start eliminating
    time += 1
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
        # else check if attributes are the same or not
        else:
            if goal_attr[x] == guess_attr[x]:
                compared.append(True)
            else:
                compared.append(False)
    new_words = words.copy()
    new_attr = attr.copy()
    # run through all words/items in list and remove any that don't match the new criteria
    for x in attr:
        for i in range(len(compared) - 1):
            if isinstance(compared[i], str):
                # if goal > guess, remove any words/items that are smaller or same
                if compared[i] == ">":
                    if list(x.values())[i] <= list(guess_attr.values())[i]:
                        print(words[attr.index(x)], "eliminated")
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
                # if goal < guess, remove any words/items that are bigger or same
                else:
                    if list(x.values())[i] >= list(guess_attr.values())[i]:
                        print(words[attr.index(x)], "eliminated")
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
            # remove any words/items that dont have the same non-numbered attribute
            else:
                if compared[i] == True:
                    if list(x.values())[i] != list(guess_attr.values())[i]:
                        print(words[attr.index(x)], "eliminated")
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
                else:
                    if list(x.values())[i] == list(guess_attr.values())[i]:
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    if len(new_words) != len(words):
        print("Words Left: ", new_words)
    return eliminate(new_words, new_attr, goal, rng_guess(new_words), time)

def human_evaluate(og_words, words, og_attr, attr, goal, time):
    # if guess word is same as goal word, found it
    if time > 1:
        guess = str(input("Guess a new word: "))
    else:
        guess = str(input())
    if guess not in og_words:
        print("Please try again, remember to use capitals and punctuation if needed...")
        human_evaluate(og_words, og_words, og_attr, og_attr, goal, time)
    if goal == guess:
        return guess, time
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
        # else check if attributes are the same or not
        else:
            if goal_attr[x] == guess_attr[x]:
                compared.append(True)
            else:
                compared.append(False)
    #print(guess, compared)
    result = dict()
    for i in range(len(compared)):
        if not isinstance(list(og_attr[og_words.index(guess)].values())[i], list):
            if isinstance(compared[i], bool):
                if compared[i] == True:
                    result[list(og_attr[og_words.index(guess)].values())[i]] = "Correct"
                elif compared[i] == False:
                    result[list(og_attr[og_words.index(guess)].values())[i]] = "Incorrect"
            else:
                result[list(og_attr[og_words.index(guess)].values())[i]] = compared[i]
        else:
            if isinstance(compared[i], bool):
                if compared[i] == True:
                    result[list(og_attr[og_words.index(guess)].keys())[i]] = "Correct"
                elif compared[i] == False:
                    result[list(og_attr[og_words.index(guess)].keys())[i]] = "Incorrect"
            else:
                result[list(og_attr[og_words.index(guess)].keys())[i]] = compared[i]
    print(result)
    new_words = words.copy()
    new_attr = attr.copy()
    # run through all words/items in list and remove any that don't match the new criteria
    if guess in words:
        for x in attr:
            for i in range(len(compared)):
                if isinstance(compared[i], str):
                    # if goal > guess, remove any words/items that are smaller or same
                    if compared[i] == ">":
                        if list(x.values())[i] <= list(guess_attr.values())[i]:
                            new_words.remove(words[attr.index(x)])
                            new_attr.remove(x)
                            break
                    # if goal < guess, remove any words/items that are bigger or same
                    else:
                        if list(x.values())[i] >= list(guess_attr.values())[i]:
                            new_words.remove(words[attr.index(x)])
                            new_attr.remove(x)
                            break
                # remove any words/items that dont have the same non-numbered attribute
                else:
                    if compared[i] == True:
                        if list(x.values())[i] != list(guess_attr.values())[i]:
                            new_words.remove(words[attr.index(x)])
                            new_attr.remove(x)
                            break
                    else:
                        if list(x.values())[i] == list(guess_attr.values())[i]:
                            new_words.remove(words[attr.index(x)])
                            new_attr.remove(x)
                            break
    print("Would you like to see the new list? [Y/N]")
    see_list = input()
    if see_list == "Y" or see_list == "y":
        print(new_words)
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    return human_evaluate(og_words, new_words, og_attr, new_attr, goal, time)

# main function, read json file into list of words/items. Then plays the game
def htn(json, word):
    ## NLP usage
    snli_jsonl_path = "./snli_1.0/snli_1.0_train.jsonl"  # Adjust this path to your SNLI JSONL file location
    glove_model_path = "./glove.6B/glove.6B.300d.txt"  # Adjust this path to your GloVe file location
    
    snli_data = load_jsonl(snli_jsonl_path)
    word_vectors = load_glove_vectors(glove_model_path)

    # Example output
    # output_similarity("dog", "cat", word_vectors)

    # End of NLP usage
    
    # words is word bank in list form, attr is list of their respective attributes
    # words and attr share the same index
    words, attr = create_dicts(json)
    # choose goal word by randomly selecting word/item from word bank
    goalword = word
    time = 1

    # guess = half_eliminate(words, attr) [EXAMPLE]
    guess = rng_guess(words)
    final, time = eliminate(words, attr, goalword, guess, time)
    print("Final Guess is:", final)
    print("Number of Guesses:", time)


def main():
    # open and collect dict from json file
    words_filename = 'arknights.json'
    print("Using", words_filename)

    with open(words_filename) as f:
        data = json.load(f)
    
    # words is word bank in list form, attr is list of their respective attributes
    # words and attr share the same index
    words, attr = create_dicts(data)

    # choose goal word by randomly selecting word/item from word bank
    goalword = random.choice(words)
    input1 = int(input("Enter 1 for bot\nEnter 2 for human: "))
    time = 1
    if input1 == 1:
        print("Goal is", goalword)
        # guess = half_eliminate(words, attr) [EXAMPLE]
        guess = rng_guess(words)
        final, time = eliminate(words, attr, goalword, guess, time)
        print("Final Guess is:", final)
        print("Number of Guesses:", time)
        input2 = input("Play Again? [Y/N]: ")
        if input2 == "Y" or input2 == "y":
            main()
        return
    elif input1 == 2:
        print("\nGuess a word from the following list:")
        print(words)
        final, time = human_evaluate(words, words, attr, attr, goalword, time)
        print("Congrats, the goal word is:", final)
        print("Number of Guesses:", time)
        input2 = input("Play Again? [Y/N]: ")
        if input2 == "Y" or input2 == "y":
            main()
        return
    else:
        print("Please input 1 or 2...")
        main()
        return

if __name__ == '__main__':
    main()