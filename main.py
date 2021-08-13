"""
An attempt at generating fake words.

The idea is based on the idea of Markov chains - given the last 2 letters, what is the most likely next letter?
Obviously this isn't perfect, but it's pretty simple to implement and train.
"""
import word
word.read_from_file()
length_prefix = [0]
for l in word.lengths:
    length_prefix.append(length_prefix[-1] + l)
max_end = max(y/(x+y+1) for x, y in word.endings.values())

import random
def generate_word():
    letters = [chr(random.choice(range(ord('a'), ord('z')+1)))]
    while True:
        c2 = "".join(letters[-2:])
        # the word ends with higher probability as 1) the word gets longer and 2) a particular digram is ended in more
        # pretty jank but the results... kind of work?
        p = (length_prefix[min(len(letters), len(length_prefix)-1)]/(length_prefix[-1]+1) \
            * (word.endings[c2][True]/sum(word.endings[c2] + [1])/max_end))**0.5
        fq = word.frequencies[c2]
        
        if random.random() < p:
            break
            
        letters.append(random.choices(list(fq.keys()), list(fq.values()), k=1)[0])
    return "".join(letters)

while True:
    print(generate_word(), end="")
    input()