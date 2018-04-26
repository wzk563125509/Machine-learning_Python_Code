from pprint import pprint
from random import shuffle

values = [ x for x in range(1,11)] + 'Jack Queen King'.split()
suits = 'diamonds clubs hearts spades'.split()
deck = ['%s of %s' %(v,s) for v in values for s in suits]
shuffle(deck)
for i in range(4):
    print('Player %s :' %(i+1))
    pprint(deck[i*12:(i+1)*12])
    print('')
