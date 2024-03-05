import heapq

weights = {
    'length': 0.8,
    'tone': 1.0,
    'is_palindrome': 2.0,
    'has_prefix': 1.2,
    'has_suffix': 1.2
}


class WordNode:
    def __init__(self, word, part_of_speech, length, tone, is_palindrome, has_prefix, has_suffix):
        self.word = word
        self.part_of_speech = part_of_speech
        self.length = length
        self.tone = float(tone)
        self.is_palindrome = is_palindrome
        self.has_prefix = has_prefix
        self.has_suffix = has_suffix

    def __lt__(self, other):
        # Define the comparison method for heapq
        # You can adjust this based on the priority criteria for your search
        return self.tone < other.tone

def heuristic(a, b, weights):
    # Euclidean distance based on attribute differences with weights
    diff_length = abs(a.length - b.length) * weights['length']
    diff_tone = abs(a.tone - b.tone) * weights['tone']
    diff_palindrome = (a.is_palindrome != b.is_palindrome) * weights['is_palindrome']
    diff_prefix = (a.has_prefix != b.has_prefix) * weights['has_prefix']
    diff_suffix = (a.has_suffix != b.has_suffix) * weights['has_suffix']

    return math.sqrt(diff_length**2 + diff_tone**2 + diff_palindrome**2 + diff_prefix**2 + diff_suffix**2)

def transition_cost(current, next_node):
    # You can customize this based on your specific requirements
    # Here, we use a simple cost based on the length difference
    return abs(current.length - next_node.length)

def astar_search(initial_word, destination_word, word_graph):
    start_node = WordNode(**word_graph[initial_word])
    goal_node = WordNode(**word_graph[destination_word])

    open_set = [(0, start_node)]  # Priority queue with initial cost
    came_from = {}  # Dictionary to store the backpointer

    g_score = {start_node: 0}

    while open_set:
        _, current_node = heapq.heappop(open_set)

        if current_node == goal_node:
            # Reconstruct the path
            path = []
            while current_node in came_from:
                path.append(current_node.word)
                current_node = came_from[current_node]
            path.append(start_node.word)
            return path[::-1]

        for neighbor_word, neighbor_attributes in word_graph.items():
            neighbor_node = WordNode(**neighbor_attributes)
            tentative_g_score = g_score[current_node] + transition_cost(current_node, neighbor_node)

            if neighbor_node not in g_score or tentative_g_score < g_score[neighbor_node]:
                g_score[neighbor_node] = tentative_g_score
                priority = tentative_g_score + heuristic(neighbor_node, goal_node)
                heapq.heappush(open_set, (priority, neighbor_node))
                came_from[neighbor_node] = current_node

    return None  # No path found

# Example usage:
word_graph = {
    "start": {"part_of_speech": "noun", "length": 5, "tone": "0.2", "is_palindrome": False, "has_prefix": False, "has_suffix": True},
    "middle": {"part_of_speech": "verb", "length": 6, "tone": "0.54", "is_palindrome": False, "has_prefix": False, "has_suffix": True},
    "end": {"part_of_speech": "adjective", "length": 4, "tone": "0.8", "is_palindrome": True, "has_prefix": False, "has_suffix": True}
}

path = astar_search("start", "end", word_graph)
print(path)
