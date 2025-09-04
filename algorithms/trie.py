class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.full_titles = []  # Store full titles at the end nodes

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # Insert all possible suffixes
        for i in range(len(word)):
            current_node = self.root
            for char in word[i:].lower():  # Convert to lowercase to handle case-insensitivity
                if char not in current_node.children:
                    current_node.children[char] = TrieNode()
                current_node = current_node.children[char]
            current_node.is_end_of_word = True
            current_node.full_titles.append(word)

    def search(self, substring):
        current_node = self.root
        for char in substring.lower():  # Convert to lowercase to handle case-insensitivity
            if char not in current_node.children:
                return []
            current_node = current_node.children[char]

        # Collect all full titles starting from this node
        results = []
        self._collect_full_titles(current_node, results)
        return results

    def _collect_full_titles(self, node, results):
        if node.is_end_of_word:
            results.extend(node.full_titles)
        
        for char, child_node in node.children.items():
            self._collect_full_titles(child_node, results)
