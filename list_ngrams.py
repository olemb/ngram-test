#!/usr/bin/env python
from __future__ import print_function

import sys
import shelve

storage = shelve.open('ngram_count.shelve')
print(len(storage), 'distinct n-grams')

for ngram in storage:
    print(ngram, storage[ngram])
