#Navigate in command prompt to location of nlp file, the use the command below to start the NLP Server locally
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
import string
import sys
import os
import csv
from pycorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

nlp = StanfordCoreNLP('http://localhost:9000')

sys.argv.pop(0)

with open('custom_stopwords.txt') as e:
    stopwordList=e.read()+','.join(set(stopwords.words('english')))

def oppositeDictionary(negT, outputDep): #Generates the list of words that can recieve affirmative transformation. (Does not work on nouns or verbs)
    for q in outputDep['sentences']:
        for y in q['basicDependencies']:
            if y['dep']=="neg":
                negWord = wn.synsets(y['governorGloss'])
                nW="1"
                for synset in negWord:
                    if str(synset).split(".")[1].split(".")[0] =='a':
                        nW=str(synset).split("'")[1].split("'")[0]
                        break
                if nW!="1":
                    nW= wn.synset(nW)
                    negT.update({str(y['governorGloss']):str(nW.lemmas()[0].antonyms()).split("'")[1].split(".")[0]})
    negT.update({'go':'stay'})

def negCheck(negT, string):
    negWord = wn.synsets(string)
    nW="1"
    val=True
    for synset in negWord:
        if str(synset).split(".")[1].split(".")[0] =='a':
            nW=str(synset).split("'")[1].split("'")[0]
            break
    if nW!="1":
        val=False
    return val

negT = {}
for file in sys.argv:
    clname = file[:-4] + "_concepts.txt"
    with open(file,'r') as f: #Reads in sentences from answer_set.txt. Removes punctuation, and annotates
        gfname = file[:-4] + "_grades.txt"
        with open(gfname,'r') as g:
            grades = g.readlines()
            with open(clname,'w') as t:
                lines = f.readlines()
                for i in range(0,len(lines)):
                    input=lines[i]
                    grade=str(grades[i])
                    input = ''.join(input.rstrip()+'\n')
                    input = input.lower() #Makes all uppercase letters lowercase.
                    input = input.replace(".", "_")
                    input = input.replace("?", "_")
                    input = input.replace("!", "_")
                    while "_\n" in input:
                        input = input.replace("_\n", "\n")
                    input = input.replace("\n", "+")

                    for z in grade:
                        grade = grade.rstrip()
                    punctuationString = "!#$%&'()*,-./:;<=>?@[]^`{|}~"
                    output = nlp.annotate(input.translate(None, punctuationString), properties={'annotators': 'tokenize,depparse,lemma', 'outputFormat': 'json'})
                    notEmpty=False
                    oppositeDictionary(negT, output)

                    for s in output['sentences']:
                        if grade == '':
                            grade='0'
                        roughS=str(grade).zfill(3)+" || "

                        nT = []
                        for y in s['basicDependencies']: #Collects the list of words in the sentence that need to be negated
                            if y['dep']=="neg":
                                nT.append(y['governor'])

                        count=0
                        for w in s["tokens"]:
                            count=count+1
                            if count in nT:
                                if negCheck(negT, w["word"])!=True: #If the word can be negated, and needs to be negated, negate it
                                    roughS=roughS+negT[w["word"]]+" "
                            else:
                                roughS=roughS+w["lemma"]+" "
                        if roughS[0:1]==" _":
                            roughS=roughS[1:]
                        roughS=roughS.split()
                        roughS = [word for word in roughS if word not in stopwordList] #Removes stopwords from the line
                        roughS = ', '.join(roughS)
                        roughS = roughS.replace('_,','|')
                        roughS = roughS.replace(', |',' |')
                        roughS = roughS.replace('||,','||')
                        roughS = roughS.replace('|| | ','|| ')
                        t.write(roughS+"\n")

