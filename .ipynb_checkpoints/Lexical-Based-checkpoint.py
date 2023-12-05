import sqlite3
import time
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import ngram
import contractions
import os
import pandas as pd

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

dataset = pd.read_csv('newdata.csv', encoding='iso-8859-1')

def normalize_text(sentence):
    if isinstance(sentence, str):
        # Convert to lowercase
        normalized_text = sentence.lower()

        # Remove special characters, punctuations, and extra white spaces
        normalized_text = re.sub(r'[^\w\s]', '', normalized_text)
        normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

        # Expand contractions
        normalized_text = contractions.fix(normalized_text)

        # Remove leading/trailing white spaces
        normalized_text = normalized_text.strip()

        return normalized_text
    else:
        # Handle non-string values (e.g., floats) by converting them to an empty string
        return ''

sentences = dataset['Headline']

total_rows = len(dataset)
correct_predictions = 0

for index, row in dataset.iterrows():
    data = normalize_text(row['Headline'])
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

    if sentCounter > 0 and row['sentiment'] == 'Positive':
        correct_predictions += 1
    elif sentCounter == 0 and row['sentiment'] == 'Neutral':
        correct_predictions += 1
    elif sentCounter < 0 and row['sentiment'] == 'Negative':
        correct_predictions += 1

accuracy = (correct_predictions / total_rows) * 100
print(f"Accuracy: {accuracy:.2f}%")
