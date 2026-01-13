import json
from pathlib import Path

class ElementBuilder:
    def __init__(self, json_path: Path):
        self.elements = self.load_elements(json_path)
        self.symbols = self.build_symbol_map()

    def load_elements(self, json_path: Path):
        with open(json_path, 'r') as file:
            return json.load(file)
    
    def build_symbol_map(self):
        symbol_map = {}
        for element in self.elements:
            symbol = element['symbol'].lower()
            symbol_map[symbol] = element
        return symbol_map
    
    def can_build_word(self, word: str):
        word = word.lower()
        n = len(word)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for j in range(max(0, i - 2), i):
                if dp[j] and word[j:i] in self.symbols:
                    dp[i] = True
                    break
        
        return dp[n]
    def build_word(self, word: str):
        word = word.lower()
        n = len(word)
        dp = [None] * (n + 1)
        dp[0] = []
        
        for i in range(1, n + 1):
            for j in range(max(0, i - 2), i):
                if dp[j] is not None and word[j:i] in self.symbols:
                    dp[i] = dp[j] + [self.symbols[word[j:i]]]
                    break
        
        return dp[n]
    def backtrack_word(self, word: str):
        elements = self.build_word(word)
        if elements is None:
            return None
        
        result = []
        for element in elements:
            result.append(f"{element['symbol'].capitalize()} ({element['name']})")
        
        return ' - '.join(result)
