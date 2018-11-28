
#libraries
import numpy as np
import tensorflow as tf
import re
import time


#importing dataset
lines = open("dataset/movie_lines.txt", encoding="utf-8", errors='ignore').read().split("\n")
conversations = open("dataset/movie_conversations.txt", encoding="utf-8", errors='ignore').read().split("\n")

#creating a dictionary
dic = {}
for line in lines:
    _line = line.split(" +++$+++ ")
    if len(_line) == 5:
        dic[_line[0]] = _line[4]


#creating a list of all conversations
conversations_id = []
# There are a empty conversation in the end, because of this -1
for conversation in conversations[:-1]:
    _conversation = conversation.split(" +++$+++ ")[-1][1:-1].replace("'", "").replace(" ","")
    conversations_id.append(_conversation.split(','))

#separate between questions and answers ( x and y )
questions = []
answers = []

for conversation in conversations_id:
    for i in range(len(conversation)-1):
        questions.append(dic[conversation[i]])
        answers.append(dic[conversation[i+1]])


#cleaning the text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "what is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text


word_counts = {}

clean_questions = []
for question in questions:
    _question = clean_text(question)
    clean_questions.append(_question)
    for word in _question.split(" "):
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1

clean_answers = []
for answer in answers:
    _answer = clean_text(answer)
    clean_answers.append(_answer)
    for word in _answer.split(" "):
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1


threshold = 20
word_number = 0
questionswords2int = {}
answersword2int = {}
for word, count in word_counts.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number+=1


answersword2int = questionswords2int

tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

for token in tokens:
    questionswords2int[token] = len(questionswords2int)+1
    answersword2int[token] = len(answersword2int) + 1

answersint2word = { w_i: w for w, w_i in answersword2int.items()}

questionsint2word = { w_i: w for w, w_i in answersword2int.items()}

for i in range(len(clean_answers)):
    clean_answers[i] += " <EOS>"

code_questions = []
for question in clean_questions:
    _question = []
    for word in question.split():
        if word not in questionswords2int:
            _question.append(questionswords2int["<OUT>"])
        else:
            _question.append(questionswords2int[word])
    code_questions.append(_question)

code_answers = []
for answers in clean_answers:
    _answer = []
    for word in answers.split():
        if word not in answersword2int:
            _answer.append(answersword2int["<OUT>"])
        else:
            _answer.append(answersword2int[word])
    code_answers.append(_answer)


