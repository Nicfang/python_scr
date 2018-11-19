#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections
import numpy as np

card = collections.namedtuple('card',['rank','suit'])
# print(card)

class Frenchdeck:

    ranks = [str(n) for n in range(2,11) + list('JQKA')]
    suits = 'spades diamonds clubs hearts'.split()

def __int__(self):
    self._cards = [card(rank,suit) for suit in self.suits
                   for rank in self.ranks]
    print self._cards

def __len__(self):
    return len(self._cards)

def __getitem__(self,position):
    return self._cards[position]

beer_card = card(['7',13],['diamonds','hearts'])
print(len(beer_card))
print(beer_card)

# print __len__(Frenchdeck())

a = []
for i in range(2,11) + list('JQKA'):
    for x in 'spades diamonds clubs hearts'.split():
        a.append(i)
        a.append(x)
print len(a)

