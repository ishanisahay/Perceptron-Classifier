import sys
import json
import codecs
import string
import re
from collections import Counter
from decimal import Decimal
import ast
import cPickle as pickle
import math

fw = codecs.open("percepoutput.txt", 'w', 'utf-8')

stopWords = []
stopWords.append("i")
stopWords.extend(
    ("me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "he", "him"))
stopWords.extend(("his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they"))

stopWords.extend(
    ("them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those"))
stopWords.extend(
    ("am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did"))
stopWords.extend((
    "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at",
    "by", "for"))
stopWords.extend(("why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same"))
stopWords.extend(("so", "than", "too", "very", "can", "will", "just", "should", "now"))
stopWords.extend(('the', 'for', 'had', 'and', 'to', 'a', 'was', 'in', 'of', 'you', 'is', 'it', 'at', 'with', 'they',
                  'on', 'our', 'be', 'as', 'there', 'an', 'or', 'this', 'my', 'that'))


def classifyAveraged(data, probability):
    avgVector = probability["avgVector"]
    avgVector2 = probability["avgVector2"]
    avgTF = probability["avgTF"]
    avgPN = probability["avgPN"]

    line = data

    words = line.split(" ")
    temp = []
    for word in words:
        wordLower = word.lower()
        puncChar = set(string.punctuation)
        wordNew = ''.join(ch for ch in wordLower if ch not in puncChar)
        if wordNew in stopWords:
            continue
        temp.append(wordNew)

    wordlines = Counter(temp)

    val = 0
    for w in wordlines:
        if w in avgVector:
            val += avgVector[w] * wordlines[w]
    val += avgTF
    val2 = 0
    for w in wordlines:
        if w in avgVector2:
            val2 += avgVector2[w] * wordlines[w]
    val2 += avgPN

    fw.write(words[0])
    fw.write(" ")
    if val < 0:
        fw.write("Fake")
    else:
        fw.write("True")
    fw.write(" ")
    if val2 < 0:
        fw.write("Neg")
    else:
        fw.write("Pos")
    fw.write("\n")


def classifyVanilla(data, probability):

    wordVector = probability["wVector"]
    wordVector2 = probability["wVector2"]
    biasTF = probability["biasTF"]
    biasPN = probability["biasPN"]

    line = data
    words = line.split(" ")
    temp = []
    for word in words:
        wordLower = word.lower()
        puncChar = set(string.punctuation)
        wordNew = ''.join(ch for ch in wordLower if ch not in puncChar)
        if wordNew in stopWords:
            continue
        temp.append(wordNew)

    feature_words = Counter(temp)

    val = 0
    for w in feature_words:
        if w in wordVector:
            val += (wordVector[w] * feature_words[w])
    val += biasTF
    val2 = 0
    for w in feature_words:
        if w in wordVector2:
            val2 += (wordVector2[w] * feature_words[w])
    val2 += biasPN

    fw.write(words[0])
    fw.write(" ")
    if val < 0:
        fw.write("Fake")
    else:
        fw.write("True")
    fw.write(" ")
    if val2 < 0:
        fw.write("Neg")
    else:
        fw.write("Pos")
    fw.write("\n")


def main():
    fp = codecs.open(sys.argv[1], 'r', 'utf-8')
    json_contents = fp.read()
    probability = json.loads(json_contents)
    fp.close()

    fd = codecs.open(sys.argv[2], 'r', "utf-8")
    lines = fd.read().splitlines()
    if (sys.argv[1] == "vanillamodel.txt"):
        for line in lines:
            classifyVanilla(line, probability)
    elif (sys.argv[1] == "averagedmodel.txt"):
        for line in lines:
            classifyAveraged(line, probability)

    fw.close()


main()

