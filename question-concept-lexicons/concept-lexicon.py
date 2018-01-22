#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Simple concept lexicon program for short answer questions
'''
from textblob import TextBlob
from textblob import Word
from textblob.wordnet import Synset

testQuestion_1 = "The best way for a society to prepare its young people for leadership in government, industry, or other fields is by instilling in them a sense of cooperation, not competition."

blob = TextBlob(testQuestion_1)

for word, pos in blob.tags:
    #pos is in unicode format
    if pos.encode('utf-8') == 'NN' or pos.encode('utf-8') == 'VP' or pos.encode('utf-8') == 'NP':
        synsetList = Word(word)
        print("Original Word: \t" + word)
        print(synsetList.synsets)
        print("\n")

        # Check for similarity value, range [0,1]

        # for synset in synsetList.synsets:
        #     print(Synset(word).path_similarity(synset))



