#Navigate in command prompt to location of nlp file, the use the command below to start the NLP Server locally
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
import string
import sys
import os
from pycorenlp import StanfordCoreNLP
from nltk.corpus import stopwords

nlp = StanfordCoreNLP('http://localhost:9000')

sys.argv.pop(0)

with open('custom_stopwords.txt') as e:
    stopwordList=e.read()+','.join(set(stopwords.words('english')))

#stopwordList=list(set(stopwordList)).lower()
#word.lower() for word in stopwordList

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
                    output = nlp.annotate(input.translate(None, punctuationString), properties={'annotators': 'tokenize,pos,parse,lemma', 'outputFormat': 'json'})
                    notEmpty=False
                    for s in output['sentences']:
                        if grade == '':
                            grade='0'
                        gOutput=str(grade).zfill(3)+" || "
                        t.write(gOutput)
                        notEmpty=True
                        cs = False
                        for w in s["tokens"]:
                            if w["word"]=='_':
                                t.write(" | ")
                                cs=False
                            elif w["word"]=='+':
                                t.write("\n")
                                cs=False
                            elif w["word"] in stopwordList: #removes stopwords from the input
                                t.write("")
                            else:
                                if cs==False:
                                    cs=True
                                    #t.write("'%s': %s" % (w["word"], w['pos']))
                                    t.write("%s" % (w["lemma"]))
                                else:
                                    #t.write(", '%s': %s" % (w["word"], w['pos']))
                                    t.write(", %s" % (w["lemma"]))
                    if notEmpty==False:
                        t.write('\n')
