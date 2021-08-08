# Generates a random poem by walking a random tree of weighted probabilites of the next word based on an ngram
# Usage:
#   py main.py [num_lines] [ngram_size]
# [num_lines] defaults to 1 and [ngram_size] defaults to 2

from random import choice, choices
from sys import argv


def words(s):
    word = ""

    for c in s:
        if c.isalpha() or c in "'’":
            word += c
        elif word:
            yield word.lower()
            word = ""

    if word:
        yield word.lower()


class WordTree(object):
    def __init__(self, ngram_size, input_path):
        self.inner_map = {}

        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                word_iter = words(line)
                try:
                    ngram = tuple(next(word_iter) for _ in range(ngram_size))
                except RuntimeError:
                    continue

                for word in word_iter:
                    self.register(ngram, word)

                    ngram = ngram[1:] + (word,)

                self.register(ngram, None)

    def register(self, ngram, word):
        if ngram not in self.inner_map:
            self.inner_map[ngram] = {}

        self.inner_map[ngram][word] = self.inner_map[ngram].get(word, 0) + 1

    def generate(self):
        ngram = choice(list(self.inner_map))
        random_walk = " ".join(ngram)

        while ngram in self.inner_map:
            current_map = self.inner_map[ngram]
            word = choices(
                list(current_map.keys()),
                list(current_map.values()),
            )[0]

            if not word:
                break

            random_walk += " " + word
            ngram = ngram[1:] + (word,)

        return random_walk


def main():
    num_lines = 1 if len(argv) < 2 else int(argv[1])
    ngram_size = 2 if len(argv) < 3 else int(argv[2])
    word_tree = WordTree(ngram_size, "sample.txt")

    for _ in range(num_lines):
        print(word_tree.generate())


if __name__ == "__main__":
    main()
