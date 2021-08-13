import json

LETTERS = tuple(chr(i) for i in range(ord("a"), ord("z")+1))
COMBOS = ("", *LETTERS, *(x+y for x in LETTERS for y in LETTERS))

frequencies = {cb: {l:0 for l in LETTERS} for cb in COMBOS}
endings = {cb: [0,0] for cb in COMBOS}
lengths = []

def train(words):
    for word in words:
        last2 = []
        if len(lengths) - 1 < len(word):
            lengths.extend([0 for i in range(len(word)+1-len(lengths))])
        lengths[len(word)] += 1
        for i in range(len(word)):
            c = word[i]
            c2 = "".join(last2)
            frequencies[c2][c] += 1
            endings[c2][False] += 1

            last2.append(c)
            while len(last2) > 2:
                last2.pop(0)
        endings["".join(last2)][True] += 1

def write_to_file(filename="data.json"):
    with open(filename, "w") as f:
        json.dump({"frequencies": frequencies, "endings": endings, "lengths": lengths}, f)

def read_from_file(filename="data.json"):
    global frequencies, endings, lengths
    with open(filename, "r") as f:
        data = json.load(f)
        frequencies = data["frequencies"]
        endings = data["endings"]
        lengths = data["lengths"]

if __name__ == "__main__":
    import scrape
    import time
    for i in range(100):
        print(f"On iteration {i+1}")
        train(scrape.words(scrape.query(scrape.get_random_pages(50))))
        time.sleep(1)
    write_to_file()