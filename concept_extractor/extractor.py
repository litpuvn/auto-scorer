#Navigate in command prompt to location of nlp file, the use the command below to start the NLP Server locally
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
import string
import sys
import os
from pycorenlp import StanfordCoreNLP
from nltk.corpus import stopwords

nlp = StanfordCoreNLP('http://localhost:9000')

sys.argv.pop(0)

with open('editstopwords.txt') as e:
    stopwordList=e.read()+','.join(set(stopwords.words('english')))

filenum=0
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
                    for c in input:
                        input = input.replace(".", " Qjq ")
                        input = input.replace("?", " Qjq")
                        input = input.replace("!", " Qjq")
                        input = input.replace("Qjq Qjq", " Qjq")
                        input = input.replace("Qjq\n", " qJq ")
                        input = input.replace("\n", " qJq ")
                    for z in grade:
                        grade = grade.rstrip()
                    output = nlp.annotate(input.translate(None, string.punctuation), properties={'annotators': 'tokenize,pos,parse', 'outputFormat': 'json'})
                    filenum = filenum+1
                    full=False
                    gIndex=0
                    for s in output['sentences']:
                        if grade == '':
                            grade='0'
                        gOutput=str(grade)+" || "
                        t.write(gOutput)
                        gIndex=gIndex+1
                        full=True
                        cs = False
                        for w in s["tokens"]:
                            if w["word"]=='Qjq':
                                t.write(" | ")
                                cs=False
                            elif w["word"]=='qJq':
                                t.write("\n")
                                cs=False
                            elif w["word"] in stopwordList: #removes stopwords from the input
                                t.write("")
                            else:
                                if cs==False:
                                    cs=True
                                    #t.write("'%s': %s" % (w["word"], w['pos']))
                                    t.write("%s" % (w["word"]))
                                else:
                                    #t.write(", '%s': %s" % (w["word"], w['pos']))
                                    t.write(", %s" % (w["word"]))
                    if full==False:
                        t.write('\n')
    #with open(clname, 'rb+') as filehandle:
    #    filehandle.seek(-2, os.SEEK_END)
    #    filehandle.truncate()
