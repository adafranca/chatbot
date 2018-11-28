
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


print(dic)

#creating a list of all conversations
conversations_id = []
# There are a empty conversation in the end, because of this -1
for conversation in conversations[:-1]:
    _conversation = conversation.split(" +++$+++ ")[-1][1:-1].replace("'", "").replace(" ","")
    conversations_id.append(conversation.split(','))

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
    text = re.sub(r"[-()\"#/@;:<>{}+=-|.?,]", "", text)
    return text

clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))


clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
