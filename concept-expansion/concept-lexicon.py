#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Simple concept lexicon program for short answer questions
'''
import json
import sys
import csv
import Levenshtein
import os
from datetime import datetime
from textblob import Word
from stringscore import liquidmetal
from fuzzywuzzy import fuzz

sys.argv.pop(0)

manualGradesFile = 'manual-grades.csv'
maxGrade = 6

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
            anwserConceptList = []
            for sentence in sentences:
                sentenceCount += 1
                jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)] = [{}]
                jsonConcepts['a_' + str(anwserCount)][0]['Actual Grade'] = grade.strip()
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
                    for syn in finalSynsets:
                        if syn not in anwserConceptList:
                            anwserConceptList.append(syn)  # Entire list of concpets and common words
                    jsonConcepts['a_' + str(anwserCount)][0]['s_' + str(sentenceCount)][0][concept.strip()] = finalSynsets # Adds list of synanonms to concept

            # Iterate through manual data & post score
            with open(manualGradesFile, "rb") as f:
                lines = csv.DictReader(f)
                highestGrade = 0.0
                for line in lines:
                    gradeList = line['Correct concepts (reasoning on the given grade)'].split(" ") # List of high scoring answers
                    calcGrade = Levenshtein.ratio("".join(gradeList), "".join(anwserConceptList))
                    if calcGrade > highestGrade:
                        highestGrade = calcGrade

                jsonConcepts['a_' + str(anwserCount)][0]['Calculated Grade'] = int(highestGrade * maxGrade)

    jsonFileName = "output-files\\" + file.split(".")[0] + "-OUTPUT.json"

    jf = open(jsonFileName, "w")
    jf.write(json.dumps(jsonConcepts, sort_keys=True))