from flair.data import Sentence
from flair.nn import Classifier

# https://flairnlp.github.io/docs/intro

# make a sentence
sentence = Sentence('I love Berlin and New York.')

# load the sentiment tagger
tagger = Classifier.load('sentiment')

# run sentiment analysis over sentence
tagger.predict(sentence)

# print the sentence with all annotations
print(sentence)
