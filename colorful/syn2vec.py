# ok here's the idea
# build a synonym network of the english language, so its basically a graph of all words, with edges between words that are synonyms
# then you convert this graph into some x-dimensional vector representation, where words that have many connections are closer together
# something like a simulation where each connected word exerts some amount of force on its neighbors, so similar words get pulled into similar clusters
from nltk.corpus import wordnet
import pandas as pd

_nrc_f = open('nrc.txt', 'r+')
_lex_df = pd.read_csv(_nrc_f, names=["word", "emotion", "association"],
                            sep=r'\t', engine='python')

words = list(_lex_df['word'])

network = {}
def add_edge(network, word1, word2):
    if word1 in network:
        network[word1].add(word2)
    else:
        network[word1] = set([word2])
    if word2 in network:
        network[word2].add(word1)
    else:
        network[word2] = set([word1])

for word in words:
    if type(word) != type(''):
        word = 'null'
    for sense in wordnet.synsets(word):
        for syn in sense.lemma_names():
            add_edge(network, word, syn)

print(network)