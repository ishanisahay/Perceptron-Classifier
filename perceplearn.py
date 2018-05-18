import sys
import json
import codecs
import string
import re
from collections import Counter
from collections import OrderedDict
from decimal import Decimal
import cPickle as pickle
import math

'''class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)'''

def train(list_of_lines, feature_counter, uniqueWords):
    j = 0
    bias = 0
    wordVector = {}
    uVector = {}
    avgVector = {}
    beta = 0
    c = 1


    bias2 = 0
    wordVector2 = {}
    uVector2 = {}
    avgVector2 = {}
    beta2 = 0
    #c = 1

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
    stopWords.extend((
                     "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only",
                     "own", "same"))
    stopWords.extend(("so", "than", "too", "very", "can", "will", "just", "should", "now"))
    stopWords.extend(('the', 'for', 'had', 'and', 'to', 'a', 'was', 'in', 'of', 'you', 'is', 'it', 'at', 'with', 'they',
                      'on', 'our', 'be', 'as', 'there', 'an', 'or', 'this', 'my', 'that'))


    for z in uniqueWords:
        wordVector[z] = 0
        uVector[z] = 0
        avgVector[z] = 0
        wordVector2[z] = 0
        uVector2[z] = 0
        avgVector2[z] = 0

    for j in range(25):
        for k, v in list_of_lines.items():
            words = v.split()
            if (words[2] == 'Pos'):
                y = 1
            else:
                y = -1
            if (words[1] == 'True'):
                y2 = 1
            else:
                y2 = -1

            a = 0
            a2 = 0
            for x in range(3, len(words)):
                word = words[x].lower()
                puncChar = set(string.punctuation)
                wordFinal = ''.join(ch for ch in word if ch not in puncChar)
                if wordFinal in stopWords:
                    continue
                a += feature_counter[k][wordFinal] * wordVector[wordFinal]
                a2 += feature_counter[k][wordFinal] * wordVector2[wordFinal]

            a = a + bias
            a2 = a2 + bias2
            feature_words = feature_counter[k].keys()
            if (a * y <= 0):
                for w in feature_words:
                    wordVector[w] += y * feature_counter[k][w]
                    uVector[w] += y * c * feature_counter[k][w]
                bias += y
                beta += y * c

            if (a2 * y2 <= 0):
                for w in feature_words:
                    wordVector2[w] += y2 * feature_counter[k][w]
                    uVector2[w] += y2 * c * feature_counter[k][w]
                bias2 += y2
                beta2 += y2 * c

            c += 1


    for w in avgVector:
        avgVector[w] = float(wordVector[w]) - (float(uVector[w]) / float(c))
    avgbias = float(bias) - (float(beta) / float(c))

    for w in avgVector2:
        avgVector2[w] = float(wordVector2[w]) - (float(uVector2[w]) / float(c))
    avgbias2 = float(bias2) - (float(beta2) / float(c))


    '''for w in avgVector:
        avgVector[w] = Decimal(wordVector[w]) - (Decimal(uVector[w]) / Decimal(c))
    avgbias = Decimal(bias) - (Decimal(beta) / Decimal(c))

    for w in avgVector2:
        avgVector2[w] = Decimal(wordVector2[w]) - (Decimal(uVector2[w]) / Decimal(c))
    avgbias2 = Decimal(bias2) - (Decimal(beta2) / Decimal(c))'''

    return wordVector, bias, avgVector, avgbias, wordVector2, bias2, avgVector2, avgbias2


def main():
    fp = codecs.open(sys.argv[1], 'r', "utf-8")
    # lines = OrderedDict()
    lines = fp.read().splitlines()
    fp.close()
    list_of_lines = OrderedDict()
    allWords = []
    weightTF = {}
    weightPN = {}
    bias1 = 0
    bias2 = 0

    stopWords = []

    for line in lines:
        words = line.split()
        id = words[0]
        list_of_lines[id] = line

    feature_words_id = OrderedDict()
    feature_words_count_id = OrderedDict()

    for k, v in list_of_lines.items():
        id = k
        words_in_line = v.split()
        feature_words_id[id] = []
        for i in range(3, len(words_in_line)):
            word = words_in_line[i].lower()
            puncChar = set(string.punctuation)
            wordFinal = ''.join(ch for ch in word if ch not in puncChar)

            feature_words_id[id].append(wordFinal)
            allWords.append(wordFinal)

        feature_words_count_id[id] = Counter(feature_words_id[id])
    uniqueWords = Counter(allWords).keys()

    weightPN, biasPN, avgPN, avgbiasPN, weightTF, biasTF, avgTF, avgbiasTF = train(list_of_lines, feature_words_count_id, uniqueWords)

    fw = codecs.open('vanillamodel.txt', 'w', 'utf-8')
    fw2 = codecs.open('averagedmodel.txt', 'w', 'utf-8')
    myobj = json.dumps({'wVector': weightTF, 'wVector2': weightPN, 'biasTF': biasTF, 'biasPN': biasPN})
    fw.write((myobj))
    fw.close()

    myobj2 = json.dumps({'avgVector': avgTF, 'avgVector2': avgPN, 'avgTF': avgbiasTF, 'avgPN': avgbiasPN})
    fw2.write(myobj2)
    fw2.close()


main()

