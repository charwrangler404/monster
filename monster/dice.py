#!/usr/bin/env python3
from random import randint

def dX(n, x):
    results = []
    for i in range(n):
        results.append(randint(1, x))
    return results