#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Simple concept lexicon program for short answer questions
'''
import json
import sys
import csv
import os
from datetime import datetime
from textblob import Word
from stringscore import liquidmetal
from fuzzywuzzy import fuzz

sys.argv.pop(0)

fileName = 'test_concepts.txt'
jsonOutputFile = 'json_concepts.json'
manualGradesFile = 'manual-grades.csv'


# Create concept expansion json file
for file in sys.argv:
    jsonConcepts = {}
    anwserCount = 0
    with open(file) as f:
        for answer in f:
            anwserCount += 1
            jsonConcepts['a_' + str(anwserCount)] = [{}]
            sentences = answer.split("||")[1].split("|")
            grade = answer.split("||")[0]
            sentenceCount = 0
            for sentence in sentences:
                sentenceCount += 1
                jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)] = [{}]
                jsonConcepts['a_' + str(anwserCount)][0]['grade'] = grade.strip()
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
                    jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)][0][concept.strip()] = finalSynsets # Adds list of synanonms to concept

                    # Iterate through manual data & post score
                    print(finalSynsets)
                    with open(manualGradesFile, "rb") as f:
                        lines = csv.DictReader(f)
                        for line in lines:
                            gradeList = line['Correct concepts (reasoning on the given grade)'].split(" ")
                            fScore = fuzz.ratio(finalSynsets, gradeList)

                            match = set(finalSynsets) & set(gradeList)
                            print("Fuzz: {}".format(fScore))
                            print("Own: {}".format((len(match)/float(len(finalSynsets)) * 100 + len(match)/float(len(gradeList)) * 100) / float(2)))

    jsonFileName = "output-files\\" + file.split(".")[0] + "-OUTPUT.json"

    jf = open(jsonFileName, "w")
    jf.write(json.dumps(jsonConcepts, sort_keys=True))

# Calculate score comparison with manual grade concepts

testA = "yes they all go into the ground, but aventually they all turn into water vapor. (it could take a long time though)"
testB = "rain snow wet cold dangerous inside"
testC = "ground water vapor wet"
testD = "cold snowy wet"
testE = "ground"

match = set(testB.split(" ")) & set(testD.split(" "))

print("Percent of concepts found in anwser {}%".format(len(match)/float(len(testD.split(" "))) * 100))
print("Percent of concepts found in graded anwser {}%".format(len(match)/float(len(testB.split(" "))) * 100))
print("Calculate Fuzz Ratio: {}".format((len(match)/float(len(testD.split(" "))) * 100 + len(match)/float(len(testB.split(" "))) * 100) / float(2)))

print(fuzz.ratio(testB.split(" "), testD.split(" ")))