import csv 
import sys
import string

enlgish = []
spanish = []

translation = {}

with open('spanish2english.tsv') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    # wordList = list(reader)
    for row in reader:
        noun = "[Noun]"
        noun2 = "[noun]"
        verb = "[Verb]"
        adjective = "[Adjective]"
        adverb = "[Adverb]"
        pronoun = "[Pronoun]"
        prep ="[Preposition]"
        
        if len(row) > 1:
            #print(row[0])
            enlgish.append(row[0])
            
            spa = row[1]
            spa = spa.replace(noun, "")
            spa = spa.replace(noun2,"")
            spa = spa.replace(verb, "")
            spa = spa.replace(adjective, "")
            spa = spa.replace(adverb, "")
            spa = spa.replace(pronoun, "")
            spa = spa.replace(prep, "")
            spa = spa.split('(', 1)[0]
            spa = spa.split('/', 1)[0]
            #print(spa)
            spanish.append(spa)
    
    #print(len(spanish))
    #print(len(enlgish))
    end = len(spanish)
    for i in range(0, len(spanish)):
        translation[spanish[i]] = enlgish[i]
    
    
    #print(translation)
    
inFile = open(sys.argv[1])
toTranslate = inFile.readlines()

outFile = open('./translatedText.txt', "w")

for line in toTranslate:
    words = line.split(' ')
    for word in words:
        word = word.lower()
        # word = word.translate(string.punctuation)
        word = word.replace(',', "")
        word = word.replace('\n', "")
        print(word)
        print("translation: ")
        t = translation[word]
        outFile.write(t + " ")
        print(t)
    print(line)

    
