import json
import numpy as np

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

# Example usage
snli_jsonl_path = "./snli_1.0/snli_1.0_train.jsonl"  # Adjust this path to your SNLI JSONL file location
glove_model_path = "./glove.6B/glove.6B.300d.txt"  # Adjust this path to your GloVe file location

snli_data = load_jsonl(snli_jsonl_path)
word_vectors = load_glove_vectors(glove_model_path)

# Example sentences
sentence1 = "Jump"
sentence2 = "Leap"

# Tokenize and get word vectors for each sentence
tokens1 = sentence1.lower().split()
tokens2 = sentence2.lower().split()

# Calculate average vector for each sentence
vector1 = np.mean([word_vectors[token] for token in tokens1 if token in word_vectors], axis=0)
vector2 = np.mean([word_vectors[token] for token in tokens2 if token in word_vectors], axis=0)

# Calculate cosine similarity between the two sentence vectors
similarity_score = cosine_similarity(vector1, vector2)
print("Cosine Similarity Score:", similarity_score)
