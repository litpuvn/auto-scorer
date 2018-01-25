# Concept Extraction - Auto Scorer

Through the use of Stanford's NLP Java Library, this program is designed to break a student answer down into a collection of topics, for use in the generation of synsets (collections of synonyms)  for each topic.

## Compiling

Before you can compile the python file, the NLP server must first be locally hosted on your computer.
The CoreNLP .zip file can be found at the following link: 
[https://stanfordnlp.github.io/CoreNLP/download.html](https://stanfordnlp.github.io/CoreNLP/download.html)

Once the .zip file has been downloaded and unpacked, navigate to the folder in a command prompt window, and enter the below command to begin hosting the server on port 9000 locally.

`$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000`

In a seperate command prompt,
**extractor.py** requires command line arguements in order to compile the program.

**One Input File:**

`$ python extractor.py answer_set0.txt`

**Two or More Input Files:**

`$ python extractor.py answer_set0.txt answer_set1.txt`


## Input File Format

1. File Extension, .txt
2. Rows represent different answers from the same question

**Psuedo Example:**
```
answer sentence 1
answer sentence 2
answer sentence 3
```

**Genuine Example:**
```
The water will slowly evaporate over time. This water eventually condensates into clouds, and eventually precipitation.
Water can escape the ground via wells, which humans have been digging for a long time.
```

## Out File Format

This program will output a .txt file for each inputted file, with the name of the file corresponding to the order in which the files are written. For example, the command:
`$ python extractor.py answer_set0.txt answer_set1.txt`
will output two files:
`$ concept_list0.txt`
`$ concept_list1.txt`
which correspond to the concepts found in the first file and the concepts found in the second file, respectively.
Within each output file, each row represents the corresponding answer in the input file. These concepts will be seperated by commas and will maintain the same order they had in the input file. For answers with multiple sentences, the "|" character will divide the concepts of different sentences.

```
The, water, will, slowly, evaporate, time | This, water, eventually, condensates, clouds, eventually, precipitation
Water, escape, ground, via, wells, humans, digging, long, time 
``` 
