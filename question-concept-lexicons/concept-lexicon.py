#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Simple concept lexicon program for short answer questions
'''
import json
import sys
from textblob import Word


print(sys.argv)


fileName = 'test_concepts.txt'
jsonOutputFile = 'json_concepts.json'

jsonConcepts = {}

anwserCount = 0
with open(fileName) as f:
    for answer in f:
        anwserCount += 1
        jsonConcepts['a_' + str(anwserCount)] = [{}]
        sentences = answer.split("|")
        sentenceCount = 0
        for sentence in sentences:
            sentenceCount += 1
            jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)] = [{}]
            concepts = sentence.split(",")
            conceptCount = 0
            for concept in concepts:
                conceptCount += 1
                synsetList = Word(concept.strip()).synsets # .strip removes the first and last whitespaces and get the synset list
                finalSynsets = []
                for synset in synsetList:
                    synset = str(synset).split("'")[1].split(".")[0] # Cleans up the synset output: Synset('cold.n.01') -> cold
                    if synset not in finalSynsets:
                        finalSynsets.append(synset)
                jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)][0][concept] = finalSynsets # Adds list of synanonms to concept

with open(jsonOutputFile, 'w') as jf:
    jf.write(json.dumps(jsonConcepts, sort_keys=True))




