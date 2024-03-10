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

def rng_guess(words):
    guess = random.choice(words)
    return guess
    

def eliminate(words, attr, goal, guess, time):
    #print(guess)
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
        if isinstance(goal_attr[x], float):
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
            #print(words[attr.index(x)])
            if isinstance(compared[i], str):
                # if goal > guess, remove any words/items that are smaller or same
                if compared[i] == ">":
                    if list(x.values())[i] <= list(guess_attr.values())[i]:
                        #print("removing", words[attr.index(x)], "for being too small", list(x.keys())[i])
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
                # if goal < guess, remove any words/items that are bigger or same
                else:
                    if list(x.values())[i] >= list(guess_attr.values())[i]:
                        #print("removing", words[attr.index(x)], "for being too big", list(x.keys())[i])
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
            # remove any words/items that dont have the same non-numbered attribute
            else:
                if compared[i] == True:
                    if list(x.values())[i] != list(guess_attr.values())[i]:
                        #print(list(x.values())[i], list(guess_attr.values())[i])
                        #print("removing", words[attr.index(x)], "for not being the same", list(x.keys())[i])
                        new_words.remove(words[attr.index(x)])
                        new_attr.remove(x)
                        break
    #print(new_words)
    #repeat process again until found last one [Be sure to swap out what goes into the "guess" slot]
    return eliminate(new_words, new_attr, goal, rng_guess(new_words), time)

# main function, read json file into list of words/items. Then plays the game
if __name__ == '__main__':
    words_filename = 'pokemon.json'

    with open(words_filename) as f:
        data = json.load(f)
    
    words, attr = create_dicts(data)

    goalword = random.choice(words)
    print("Goal is", goalword)
    time = 0

    #guess = half_eliminate(words, attr)
    guess = rng_guess(words)
    final, time = eliminate(words, attr, goalword, guess, time)
    print("Final Guess is:", final)
    print("Number of Guesses:", time)
