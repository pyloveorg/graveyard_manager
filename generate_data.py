#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''moduł do generowania wszelkich potrzebnych danych'''
import random

def generate_password():
    '''funkcja do generowania nowego hasła w przypadku utraty poprzedniego'''
    big_letters = [chr(x) for x in range(ord('A'), ord('Z')+1)]
    low_letters = [chr(x) for x in range(ord('a'), ord('z')+1)]
    numbers = [str(x) for x in range(0, 10)]
    special = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '+']
    gen_pw = []
    for i in [random.sample(x, 2) for x in [big_letters, low_letters, numbers, special]]:
        gen_pw += i
    random.shuffle(gen_pw)
    return ''.join(gen_pw)

if __name__ == '__main__':
    print(generate_password())
