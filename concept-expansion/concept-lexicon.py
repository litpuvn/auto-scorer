#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Simple concept lexicon program for short answer questions
'''
import json
import sys
import csv
import Levenshtein
import difflib
import os
from datetime import datetime
from textblob import Word
from stringscore import liquidmetal
from fuzzywuzzy import fuzz

sys.argv.pop(0)

manualGradesFile = 'manual-grades.csv'
maxGrade = 6

# Create concept expansion json file
def createJsonFile(file):

    jsonConcepts = {}
    anwserCount = 0
    accuracyCount = 0
    accuracyList = []
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
                jsonConcepts['a_' + str(anwserCount)][0]['0_Actual Grade'] = int(grade.strip())
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
                    anwserConceptList = [x.strip(' ') for x in anwserConceptList]

                    actGrade = jsonConcepts['a_' + str(anwserCount)][0]['0_Actual Grade']
                    calculatedGrade = calcGrade(anwserConceptList)

                    jsonConcepts['a_' + str(anwserCount)][0]['3_Final Concept List'] = anwserConceptList
                    jsonConcepts['a_' + str(anwserCount)][0]['1_Calculated Grade'] = calculatedGrade

            # This next two lines are need since divison by 0 is undifined
            calculatedGrade += 1
            actGrade +=1
            if (calculatedGrade >= actGrade):
                accuracyList.append(actGrade / float(calculatedGrade))
            else:
                accuracyList.append(calculatedGrade / float(actGrade))

    print("One to One: {}".format(oneToOneAccuracy(accuracyList)))
    print("Percentage Agree: {}".format(percentageAgreement(accuracyList)))

    jsonConcepts["Grading Accuracy"] = "TESTING"

    jsonFileName = "output-files/" + file.split(".")[0] + "-OUTPUT.json"
    jf = open(jsonFileName, "w")
    jf.write(json.dumps(jsonConcepts, sort_keys=True))

    print("Json file created: {}".format(jsonFileName))

# Method 1
# Highest % number of concepts in ungraded answer found in
# the graded answer key
def calcGrade(ngCL):
    with open(manualGradesFile, "rb") as f:
        gradedAns = csv.DictReader(f)
        highestGrade = 0.0
        for gAns in gradedAns:  # Iterate through each graded answers
            gCL = gAns['Correct concepts (reasoning on the given grade)'].split(" ")  # Graded Concept List
            concMatch = 0
            for gC in gCL:  # Iterate through each concept in non-graded answer
                for ngC in ngCL:  # Iterate through each concept in graded answer
                    wordMatch = Levenshtein.ratio(gC, ngC)
                    if wordMatch > .80:
                        if (concMatch < len(gCL)):
                            concMatch += 1
            currentGrade = concMatch / float(len(gCL))  # Calculated how many nongraded Concepts were found in graded concepts list
            if currentGrade > highestGrade:
                highestGrade = currentGrade
    return int(highestGrade * maxGrade + .5) # Rounded Up

def oneToOneAccuracy(accuracyList):
    sum = 0
    for accuracy in accuracyList:
        if (accuracy == 1.0):
            sum += 1
    return (sum / float(len(accuracyList)))

def percentageAgreement(accuracyList):
    return (sum(accuracyList) / float(len(accuracyList)))


# Main
if __name__ == "__main__":

    for file in sys.argv:
        createJsonFile(file)