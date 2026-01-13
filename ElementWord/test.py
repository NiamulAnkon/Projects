from element_builder import ElementBuilder
from pathlib import Path

builder = ElementBuilder(Path('elements.json'))

words = ["Carbon", "Neon", "Bacon", "Coffee", "Science", "Hello",]

for word in words:
    if builder.can_build_word(word):
        result = builder.backtrack_word(word)
        print(f"{word}: {result}")
    else:
        print(f"{word}: Cannot be built from element symbols.")

