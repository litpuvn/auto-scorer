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
2. Place file in **../concept-expansion/..** directory
3. Rows represent unique anwsers from a short anwser question
4. Each row may contain multiple sentences, with each sentences seperated by a 
vertical bar, "|", character
5. Inbetween the vertical bar are comma seperated concepts. English words or word phrases
6. Grades are given at the beggining of each row, seperated by a double verticle line, "||".
If the **answer has not been graded**, denote that as **-1**

**Psuedo Example:**
```
grade || concept 1, concept 2 | concept 3, concept 4, concept 5 | concept 6
ungraded || concept 9
grade || concept 2 | concept 5, concept 6
```

**Genuine Example:**
```
5 || rain, snow, wet | cold, dangerous | freezing cold, icey
-1 || cold, raining | sad, dangerous, ice
3 || snowy, ice cold
```

##Out File Format

This program will output a json file that is easily parseable. Using the input 
format, *Genuine Example*, below here is a shortened JSON Pretty output file sample of the first
two rows:

* **0_grading_accuracy:** Overall accuracy of our grading program.
    Mean of when "Actual Grade" is equal "Calculated Grade"
* **Actual Grade:** Grade that was recieved by human grader
* **Calculated Grade:** Grade that was recieved by program grader
* **s_1:** Sentence one
* **a_1:** Arbitrary name convention to seperate each answer
* **s_1:** Sentence one
* **rain:** Concept one in sentence one 
* **snow:** Concept two in sentence one 
* ect...

```
{
"0_grading_accuracy": 34.1747572815534,
"a_1":[
    {
        "Actual Grade": 5,
        "Calculated Grade": 2,
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

