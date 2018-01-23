# Concept Expansions - Auto Scorer

Based on Concept Splitting output data, this program is designed to expanded on 
a collection of concepts to find synsets of each topics. Synets are a collection of
synonyms. This program will help assist with finalizing automated grades from short answer
questions, given a rubric.

## Compiling

**concept-lexicon.py** requires command-line arguements. Below are two examples 
in compiling this program:

**One Input File:**

`$ python concept-lexicon.py test-concepts_1.txt`

**Two or More Input Files:**

`$ python concept-lexicon.py test-concepts_1.txt test-concepts_2.txt`


##Input File Format

1. File Extension, .txt
2. Rows represent different answers from the same question
3. Each row may contain multiple sentences, with each sentences seperated by a 
vertical bar, "|", character
4. Inbetween the vertical bar are comma seperated concepts. English words or word phrases

**Psuedo Example:**
```
concept 1, concept 2 | concept 3, concept 4, concept 5 | concept 6
concept 9
concept 2 | concept 5, concept 6
```

**Genuine Example:**
```
rain, snow, wet | cold, dangerous | freezing cold, icey
cold, raining | sad, dangerous, ice
snowy, ice cold
```

##Out File Format

This program will output a json file that is easily parseable. Using the input 
format, *Genuine Example*, below here is a shortened JSON Pretty output file sample of the first
two rows:

* **a_1:** Answer, row 1
* **s_1:** Sentence one
* **rain:** Concept one in sentence one 
* **snow:** Concept two in sentence one 
* ect...

```
{
"a_1":[
    {
        "s_1":[
            {
                "rain":[
                    "rain"
                ],
                "snow":[
                    "snow",
                    "coke",
                    "bamboozle"
                ],
                "wet":[
                    "moisture",
                    "wet",
                    "besotted"
                ]
            }
        ],
        "s_2":[
            {
                "cold":[
                    "cold",
                    "coldness"
                ],
                "dangerous":[
                    "dangerous"
                ]
            }
        ]
     }]
 }
``` 

