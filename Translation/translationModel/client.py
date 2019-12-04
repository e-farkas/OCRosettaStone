import time
import request
import sys

def request_from_server(word):
    
    URL = ""

    # File name so that it can be temporarily stored.
    translationFile = 'translatedText.txt'

    # Reopen image and encode in base64
    # Open binary file in read mode
    fileToTranslate = open(sys.argv[1], "r")
    wordsToTranslate = fileToTranslate.readlines()
    cleanedWords = ""
    
    for line in wordsToTranslate:
        words = line.split(' ')
        for word in words:
            word = word.lower()
            # word = word.translate(string.punctuation)
            word = word.replace(',', "")
            word = word.replace('\n', "")
            cleanedWords += word
            print(cleanedWords)


    payload = {'word': cleanedWords}
    response = requests.post(url=URL, json=payload)
    prediction = response.json()

    return prediction


def main():
    
    # need to get the words from the passed in file
    phrase= ""

    prediction = request_from_server(phrase)
    
    outFile = open('translatedText.txt', "w")
    
    outFile.write(prediction)
