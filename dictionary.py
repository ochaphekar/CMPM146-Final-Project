import json
import requests
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

def get_word_sentiment(word):
    synsets = wn.synsets(word)
    
    if not synsets:
        return None
    
    # Assuming the first synset is the most common one
    synset = synsets[0]
    
    # Get the sentiment scores from SentiWordNet
    senti_synset = swn.senti_synset(synset.name())
    sentiment_score = senti_synset.pos_score() - senti_synset.neg_score()

    return sentiment_score

def contains_vowel(word):
    vowels = "aeiouAEIOU"
    return any(char in vowels for char in word)

def get_word_info(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def is_palindrome(word):
    cleaned_word = ''.join(char.lower() for char in word if char.isalnum())
    return cleaned_word == cleaned_word[::-1]

def main():
    json_file_path = "dictionary.json"  # Replace with the path to your JSON file
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    for key in json_data.keys():
        # set word length
        json_data[key]["length"] = len(key)

        # get word info to determine POS
        info = get_word_info(key)
        word_meanings = info[0]["meanings"]
        part_of_speech = []
        for m in word_meanings:
            part_of_speech.append(m["partOfSpeech"])
        json_data[key]["part_of_speech"] = part_of_speech

        # check if word is palindrome
        if is_palindrome(key):
            json_data[key]["is_palindrome"] = True
        else:
            json_data[key]["is_palindrome"] = False

        # contains vowel
        if contains_vowel(key):
            json_data[key]["contains_vowel"] = True
        else:
            json_data[key]["contains_vowel"] = False

        # get tone of word
        print("tone of", key, " is ", get_word_sentiment(key))
        json_data[key]["tone"] = get_word_sentiment(key)

    # Now, you might want to save the modified dictionary back to the file if needed
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=2)

if __name__ == "__main__":
    main()
