#!/usr/bin/env python
"""
https://www.un.org/en/documents/udhr/
"""
import sys
import shelve
import string
from collections import Counter, deque

LETTERS = set(string.lowercase) | set("'-")

def is_valid_ngram(ngram):
    """Return True if the n-gram consists only of letters."""
    for char in ngram:
        if char not in LETTERS:
            return False

    return True


def read_ngrams(filename, length):
    """Generate n-grams of length 'length' from a file."""
    ngram = deque(' ' * length)

    with open(filename) as file:
        for line in file:
            for char in line:
                ngram.popleft()
                ngram.append(char)
           
                if is_valid_ngram(ngram):
                    yield ''.join(ngram)


def store_counts(storage, counter):
    """Store n-gram count in shelve."""
    for ngram, count in counter.items():
        try:
            stored_count = storage[ngram]
        except KeyError:
            stored_count = 0
        storage[ngram] = stored_count + count

    storage.sync()
    counter.clear()


def process_file(filename, storage, ngram_length, max_mem_ngrams):
    """Count all distinct n-grams of length 'ngram_length'.
    """
    counter = Counter()

    for ngram in read_ngrams(filename, ngram_length):
        counter[ngram] += 1

        if len(counter) >= max_mem_ngrams:
            print('Reached {} distinct n-grams. Storing them away.'.format(
                    len(counter)))
            store_counts(storage, counter)

    print('{} distinct ngrams at end of run. Storing them away.'.format(
            len(counter)))
    store_counts(storage, counter)


def main():
    storage = shelve.open('ngram_count.shelve', flag='c', writeback=True)
    try:
        process_file('human_rights.text', storage=storage,
                     ngram_length=3, max_mem_ngrams=100)
    finally:
        storage.close()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
