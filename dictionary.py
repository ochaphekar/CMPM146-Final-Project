import json
import requests

def contains_a(word):
    return word.lower().count('a')

def contains_e(word):
    return word.lower().count('e')

def contains_i(word):
    return word.lower().count('i')

def contains_o(word):
    return word.lower().count('o')

def contains_u(word):
    return word.lower().count('u')

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

def letter_index(word):
    # Convert the word to lowercase to handle case insensitivity
    word = word.lower()

    # Get the first letter of the word
    first_letter = word[0]

    # Get the ASCII value of the first letter
    ascii_value = ord(first_letter)

    # Subtract the ASCII value of 'a' to get the index
    index = ascii_value - ord('a')

    return index

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
        part_of_speech = set()
        for m in word_meanings:
            part_of_speech.add(m["partOfSpeech"])
        json_data[key]["part_of_speech"] = list(part_of_speech)

        # check if word is palindrome
        if is_palindrome(key):
            json_data[key]["is_palindrome"] = True
        else:
            json_data[key]["is_palindrome"] = False

        # contains a
        json_data[key]["contains_a"] = contains_a(key)
        # contains e
        json_data[key]["contains_e"] = contains_e(key)
        # contains i
        json_data[key]["contains_i"] = contains_i(key)
        # contains o
        json_data[key]["contains_o"] = contains_o(key)
        # contains u
        json_data[key]["contains_u"] = contains_u(key)

        # get letter index
        json_data[key]["index"] = letter_index(key)

    # Now, you might want to save the modified dictionary back to the file if needed
    with open(json_file_path, 'w') as file:
        json.dump(json_data, file, indent=2)

if __name__ == "__main__":
    main()
