#Navigate in command prompt to location of nlp file, the use the command below to start the NLP Server locally
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
import string
import sys
import os
from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

#with open('stopwords.txt','r') as sw:
#    swlist = sw.read()
#    first=False
#    for line in swlist:
#        for word in line.split():
#            #swlist = swlist.replace("\n", "")
#            if first==False:
#                swlist = swlist.replace(word, "'"+word+"'")
#                first=True
#            else:
#                swlist = swlist.replace(word, ",'"+word+"'")

sys.argv.pop(0)

with open('editstopwords.txt') as e:
    stopwords=e.read()

filenum=0
for file in sys.argv:
    with open(file,'r') as f: #Reads in sentences from answer_set.txt. Removes punctuation, and annotates
        input=f.read()
        #input = input.lower() #Makes all uppercase letters lowercase.
        for c in input:
            input = input.replace(".", " Qjq")
            input = input.replace("?", " Qjq")
            input = input.replace("!", " Qjq")
            input = input.replace("\n", " qJq ")
            input = input.replace("Qjq qJq", " qJq ")
        output = nlp.annotate(input.translate(None, string.punctuation), properties={'annotators': 'tokenize,pos,parse', 'outputFormat': 'json'})
    clname = "concept_list"+str(filenum)+".txt"
    filenum = filenum+1
    with open(clname,'w') as t: #Writes to file each word, with its Part of Speech label
        #stopwords = 'what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now'
        for s in output['sentences']:
            cs = False
            for w in s["tokens"]:
                if w["word"]=='Qjq':
                    t.write(" | ")
                    cs=False
                elif w["word"]=='qJq':
                    t.write("\n")
                    cs=False
                elif w["word"] in stopwords: #removes stopwords from the input
                    t.write("")
                else:
                    if cs==False:
                        cs=True
                        #t.write("'%s': %s" % (w["word"], w['pos']))
                        t.write("%s" % (w["word"]))
                    else:
                        #t.write(", '%s': %s" % (w["word"], w['pos']))
                        t.write(", %s" % (w["word"]))
            #t.write(output['sentences'][s["index"]]['parse'])
            #t.write(" ".join(w["word"] for w in s["tokens"]))
    with open(clname, 'rb+') as filehandle:
        filehandle.seek(-2, os.SEEK_END)
        filehandle.truncate()
