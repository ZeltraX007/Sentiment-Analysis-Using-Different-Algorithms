import sqlite3
import time
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import ngram
import os

db_path = 'DataBase/knowledgeBase.db'
# Check if the directory exists, create it if not
directory = os.path.dirname(db_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# Now, connect to the database
conn = sqlite3.connect(db_path)

c = conn.cursor()

negativeWords = []
positiveWords = []
reviews = []
posCount = 0
negCount = 0
neuCount = 0
revCount = 0
orgnation = ''

ps = PorterStemmer()

sql1 = 'SELECT * FROM wordVals WHERE value <?'
sql2 = 'SELECT * FROM wordVals WHERE value >?'

def loadWordArrays():
    for negRow in c.execute(sql1,[(0)]):
        negativeWords.append(negRow[0])

    print('negative words loaded')

    for posRow in c.execute(sql2,[(0)]):
        positiveWords.append(posRow[0])
    print('positive words loaded')

def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

#print(ngramas('This place is not good',2))

loadWordArrays()
reviews = []
#print([' '.join(x) for x in ngrams('How are you',2)])

sentences = ['I hate this food',
             'I love this food',
             'bad service and not clean place',
             'tasty food',
             'Truly amazing place, with delicious food!',
             'visited for lunch, the place was crowded and seems to be popular',
             'the place had a really nice atmosphere and the food was delicious',
             'This palce has occupied the dumbest staff who has no common sense',
             'The choice was good. no doubt the food was tasty',
             'The choice was bad. no doubt the food was not tasty',
             "It's been a while since I have dined at Mango Tree but from what I remember the food is great! Service was a little bit slow but the food made up for it :D Good range of cocktails too.",
             'Good food but the service is too slow. Spent nearly 3 hours just to have dinner. Waiters confused on the order and mixed up on lot of tables.',
             'Mouth watering, tasty Indian food. My wife kids were so much interested to eat. Had a nice time with family.']

for num in sentences:
    data = num
    word_sent_tokens = word_tokenize(data)
    sentCounter = 0
    sentence = []
    for w in word_sent_tokens:
        sentence.append(w.lower())
    for eachPosWord in sentence:
        if eachPosWord in positiveWords:
            print("Positive")
            print(eachPosWord)
            sql1 = "SELECT * FROM wordVals WHERE word ==?"
            for val in c.execute(sql1,[eachPosWord]):
                sentCounter = sentCounter + val[1]
    for eachNegWord in sentence:
        if eachNegWord in negativeWords:
            print("Negative")
            print(eachNegWord)
            sql1 = "SELECT * FROM wordVals WHERE word ==?"
            for val in c.execute(sql1,[eachNegWord]):
                sentCounter = sentCounter + val[1]
    print(data)
    for g in (' '.join(x) for x in ngrams(data, 2)):
        word_tokens = word_tokenize(g)
        sent = []
        for w in word_tokens:
            sent.append(w.lower())
        if sent[0] in negativeWords and sent[1] in positiveWords:
            print(sent)
            sql1 = "SELECT * FROM wordVals WHERE word ==?"
            for val in c.execute(sql1,[sent[0]]):
                sentCounter = sentCounter + val[1]

        if sent[0] in negativeWords and sent[1] in negativeWords:
            print(sent)
            sql1 = "SELECT * FROM wordVals WHERE word ==?"
            for val in c.execute(sql1,[sent[0]]):
                print('ngram 2')
                sentCounter = sentCounter - val[1]
                sentCounter = sentCounter + 2
    for g in (' '.join(x) for x in ngrams(data, 3)):
        word_tokens = word_tokenize(g)
        sent = []
        for w in word_tokens:
            sent.append(w.lower())
        if sent[0] in negativeWords and sent[1] in positiveWords and sent[2] in positiveWords:
            print('-------neg--------')
            print(sent)
            sql1 = 'SELECT * FROM wordVals WHERE word ==?'
            for val in c.execute(sql1,[sent[0]]):
                print('ngram 3')
                sentCounter = sentCounter + val[1]
                sentCounter = sentCounter - 1

    if sentCounter > 0:
        print('This text is positive')
        print('Sent value is '+str(sentCounter))
        print('-------------------')
        posCount = posCount+1

    if sentCounter == 0:
        print('This text is neutral')
        print('Sent value is '+str(sentCounter))
        print('-------------------')
        neuCount = neuCount+1

    if sentCounter < 0:
        print('This text is negative')
        print('Sent value is '+str(sentCounter))
        print('-------------------')
        negCount = negCount+1

print('positive sentences '+str(posCount))
print('neutral sentences '+str(neuCount))
print('negative sentences '+str(negCount))