import heapq
import math
import json

weights = {
    'length': 0.8,
    'is_palindrome': 2.0,
}

class WordNode:
    def __init__(self, word, **kwargs):
        self.word = word
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __lt__(self, other):
        # Define the comparison method for heapq
        # You can adjust this based on the priority criteria for your search
        return len(self.word) < len(other.word)

def heuristic(a, b, weights):
    # Euclidean distance based on attribute differences with weights
    diff_length = abs(a.length - b.length) * weights['length']
    diff_tone = abs(a.tone - b.tone) * weights['tone']
    diff_palindrome = (a.is_palindrome != b.is_palindrome) * weights['is_palindrome']

    return math.sqrt(diff_length**2 + diff_tone**2 + diff_palindrome**2)

def transition_cost(current, next_node):
    # You can customize this based on your specific requirements
    # Here, we use a simple cost based on the length difference
    return abs(current.length - next_node.length)

def astar_search(initial_word, destination_word, attributes):
    # make a new start_node by combining initial_word and word_graph[initial_word]

    start_node = WordNode(initial_word, **attributes[initial_word]) 
    goal_node = WordNode(destination_word, **attributes[destination_word])

    open_set = [(0, start_node)]  # Priority queue with initial cost
    came_from = {}  # Dictionary to store the backpointer

    g_score = {start_node: 0}

    while open_set:
        _, current_node = heapq.heappop(open_set)

        if current_node.word == goal_node.word:
            # Reconstruct the path
            path = []
            while current_node in came_from:
                path.append(current_node.word)
                current_node = came_from[current_node]
            path.append(start_node.word)
            return path[::-1]

        for neighbor_word, neighbor_attributes in attributes.items():
            neighbor_node = WordNode(neighbor_word, **neighbor_attributes)
            tentative_g_score = g_score[current_node] + transition_cost(current_node, neighbor_node)

            if neighbor_node not in g_score or tentative_g_score < g_score[neighbor_node]:
                g_score[neighbor_node] = tentative_g_score
                priority = tentative_g_score + heuristic(neighbor_node, goal_node, weights)
                heapq.heappush(open_set, (priority, neighbor_node))
                came_from[neighbor_node] = current_node

    return None  # No path found

# currently loops between left, born, five, much, both, never reaching power

dictionary = None

# load dictionary.json to use as word_graph
with open('dictionary.json', 'r') as file:
    dictionary = json.load(file)


path = astar_search("left", "power", dictionary)
print(path)
