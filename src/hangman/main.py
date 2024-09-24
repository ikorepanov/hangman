from random import randrange

def get_random_word(fhand, default=None):
    word = default
    for i, aline in enumerate(fhand, start=1):
        if randrange(i) == 0:
            word = aline
    return word.strip()


with open('dictionary.txt') as f:
    word = get_random_word(f)
    print(word)
