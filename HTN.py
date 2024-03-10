import json
import random

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
    # repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    return eliminate(new_words, new_attr, goal, rng_guess(new_words), time)

# main function, read json file into list of words/items. Then plays the game
if __name__ == '__main__':
    # open and collect dict from json file
    words_filename = 'pokemon.json'
    with open(words_filename) as f:
        data = json.load(f)
    
    # words is word bank in list form, attr is list of their respective attributes
    # words and attr share the same index
    words, attr = create_dicts(data)

    # choose goal word by randomly selecting word/item from word bank
    goalword = random.choice(words)
    print("Goal is", goalword)
    time = 0

    # guess = half_eliminate(words, attr) [EXAMPLE]
    guess = rng_guess(words)
    final, time = eliminate(words, attr, goalword, guess, time)
    print("Final Guess is:", final)
    print("Number of Guesses:", time)
