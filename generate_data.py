#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def generate_password():
    '''funkcja do generowania nowego hasła w przypadku utraty poprzedniego'''
    BigLetters = [chr(x) for x in range(ord('A'), ord('Z')+1)]
    LowLetters = [chr(x) for x in range(ord('a'), ord('z')+1)]
    Numbers = [str(x) for x in range(0,10)]
    Special = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '+']
    pw = []
    for i in [random.sample(x, 2) for x in [BigLetters, LowLetters, Numbers, Special]]:
        pw += i
    random.shuffle(pw)
    return ''.join(pw)

if __name__ == '__main__':
    print(generate_password())