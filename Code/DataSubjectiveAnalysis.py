################################
#         INTRODUCTION         #
################################

from __future__ import division
from collections import defaultdict
from DataClean import hexadecimal_conversion as hex_con
from DataClean import unicode_clean as uni_clc

import math
import operator
import pycountry
import time
import os
import json


############################
#         FUNCTION         #
############################

def print_dictionary(language, part, sign):
    where = pycountry.languages.get(alpha_2=language.lower()).name
    print("\nPrinting the " + sign + " terms in " + where + " of the dictionary.\n")
    time.sleep(5)
    fname = open(part, 'r')
    dictionary = list(str(fname.readline()).split())
    fname.close()
    i = 0
    for item in list(dictionary):
        i += 1
        print('\t' + str(i) + ': ' + item)
    return


def new_dictionary(help, part):
    print("\n\tIMPORTANT: This method only can store ASCII characters.")
    print("\tIf you introduce a non-ASCII character, it will be converted to his equivalent.")
    print("\tIf there is no equivalent, it will be erased.")
    new_words = []
    dictionary = []
    if help is None:
        if not os.path.isfile(part):
            f_new = open(part, 'wb')
            f_new.close()
        else:
            with open(part, 'r') as FILE:
                for line in FILE:
                    for item in line.split():
                        dictionary.append(item)
        while True:
            print("\n\tIntroduce 0 if you want to stop or if you have finished.")
            term = uni_clc(hex_con(raw_input("\tIntroduce the next term: ").decode('utf8').encode('unicode_escape')))
            if term == str(0):
                break
            new_words.extend(term.lower().split())

    else:
        if not os.path.isfile(part):
            f_new = open(part, 'wb')
            f_new.close()
        else:
            with open(part, 'r') as FILE:
                for line in FILE:
                    for item in line.split():
                        dictionary.append(item)
        f_dict = open(help, 'r')
        words_en = list(str(f_dict.readline()).split())
        f_dict.close()
        print("\n\tHave you started yet?")
        where = raw_input("\tIf yes, introduce the term; if not, just press enter: ")
        start = 0
        i = 0
        for item in words_en:
            i += 1
            if where == item or where == '' or start == 1:
                start = 1
                print("\n\tIf there are synonyms or common equivalent words, separate them with a blank space.")
                print("\tIntroduce 0 if you want to stop or if you have finished.")
                print('\t' + str(i) + ": " + item)
                term = uni_clc(hex_con(raw_input('\tTranslate the term: ').decode('utf8').encode('unicode_escape')))
                if term == str(0):
                    break
                new_words.extend(term.lower().split())
    write = 0
    for i in range(len(new_words)):
        for j in range(len(dictionary)):
            if new_words[i] == dictionary[j]:
                write = 1
                break
            elif len(new_words[i]) <= len(dictionary[j]):
                for k in range(len(new_words[i])):
                    if ord(new_words[i][k]) > ord(dictionary[j][k]):
                        break
                    elif ord(new_words[i][k]) < ord(dictionary[j][k]):
                        dictionary.insert(j, new_words[i])
                        write = 1
                        break
                    elif (k == (len(new_words[i]) - 1)) and (ord(new_words[i][k]) == ord(dictionary[j][k])):
                        dictionary.insert(j, new_words[i])
                        write = 1
                        break
            else:
                for k in range(len(dictionary[j])):
                    if ord(new_words[i][k]) > ord(dictionary[j][k]):
                        break
                    elif ord(new_words[i][k]) < ord(dictionary[j][k]):
                        dictionary.insert(j, new_words[i])
                        write = 1
                        break
            if write == 1:
                break
        if write == 0:
            dictionary.append(new_words[i])
        else:
            write = 0
    with open(part, 'wb') as FILE:
        for item in dictionary:
            FILE.write(item + " ")
    return


# The Point Mutual Information (PMI) is a measure of association used in information theory and statistics.
# In contrast to Mutual Information (MI) which builds upon PMI, it refers to single events, whereas MI refers to the
# average of all possible events.
#
# PMI(t1,t2) = log(P(t1^t2)/(P(t1)*P(t2)))
#
# Also, we define the Semantic Orientation (SO) of a word as the difference between its associations with positive
# and negative words. In practice, we want to calculate "how close" a word is with terms like 'good' and 'bad'.
#
# SO(t) = Summation_t'PD(PMI(t,t')) - Summation_t'ND(PMI(t,t'))
#
# t'PD: term t' in the Positive Dictionary
# t'ND: term t' in the Negative Dictionary
#
# The PMI-based approach has been introduced as simple and intuitive, but of course it has some limitations. Some
# aspects of natural language are not captured by this approach, more notably modifiers and negation: how do we deal
# with phrases line 'not bad' (this is the opposite of just 'bad') or 'very good' (this is stronger than just 'good')?
#
# Numpy arrays instead of python dictionaries are advisable for anything bigger than an example
def subjective_analysis(fname, terms_tweets, com, language, mode, term):
    name = fname.split('.')[0].split('_')
    ext = fname.split('.')[1]
    sub_dict = name[0] + "SubjectiveDictionary_" + name[-2] + "_" + language + ".json"
    if not os.path.isfile(sub_dict):
        n_docs = 0
        with open(fname, 'r') as FILE:
            if not ext == 'json':
                next(FILE)
                for line in FILE:
                    if line != '\n':
                        n_docs += 1
            elif ext == 'json':
                for line in FILE:
                    document = json.loads(line)
                    text = document['text'].encode('unicode_escape')
                    if text != '\n':
                        n_docs += 1
        p_t = {}
        p_t_com = defaultdict(lambda: defaultdict(int))
        for term, n in terms_tweets.items():
            p_t[term] = n / n_docs
            for t2 in com[term]:
                p_t_com[term][t2] = com[term][t2] / n_docs
        # Lexicon example for positive and negative vocabulary
        # positive_words = ['good', 'nice', 'great', 'awesome', 'outstanding', 'fantastic', 'terrific', 'like', 'love']
        # negative_words = ['bad', 'terrible', 'crap', 'useless', 'hate']
        words = open('PositiveWords_' + language + '.txt', 'r')
        positive_words = list(str(words.readline()).split())
        words.close()
        words = open('NegativeWords_' + language + '.txt', 'r')
        negative_words = list(str(words.readline()).split())
        words.close()

        # Opinion Lexicon: This files contains a list of POSITIVE and NEGATIVE opinion words (or sentiment words).
        # This file and the papers can all be downloaded from
        #    http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
        # If you use this list, please cite one of the following two papers:
        #   Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
        #       Proceedings of the ACM SIGKDD International Conference on Knowledge
        #       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
        #       Washington, USA,
        #   Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing
        #       and Comparing Opinions on the Web." Proceedings of the 14th
        #       International World Wide Web conference (WWW-2005), May 10-14,
        #       2005, Chiba, Japan.
        # Notes:
        #    1. The appearance of an opinion word in a sentence does not necessarily
        #       mean that the sentence expresses a positive or negative opinion.
        #       See the paper below:
        #           Bing Liu. "Sentiment Analysis and Subjectivity." An chapter in
        #           Handbook of Natural Language Processing, Second Edition,
        #           (editors: N. Indurkhya and F. J. Damerau), 2010.
        #    2. You will notice many misspelled words in the list. They are not
        #       mistakes. They are included as these misspelled words appear
        #       frequently in social media content.
        pmi = defaultdict(lambda: defaultdict(int))
        for t1 in p_t:
            for t2 in com[t1]:
                denominator = p_t[t1] * p_t[t2]
                pmi[t1][t2] = math.log(p_t_com[t1][t2] / denominator) / math.log(2)
        semantic_orientation = {}
        for term, n in p_t.items():
            positive_assoc = sum(pmi[term][tx] for tx in positive_words)
            negative_assoc = sum(pmi[term][tx] for tx in negative_words)
            semantic_orientation[term] = positive_assoc - negative_assoc
        with open(sub_dict, 'wb') as FILE:
            json.dump(semantic_orientation, FILE)
    else:
        with open(sub_dict, 'r') as FILE:
            semantic_orientation = json.load(FILE)
    if mode == '10th':
        # noinspection PyTypeChecker
        semantic_sorted = sorted(semantic_orientation.items(), key=operator.itemgetter(1), reverse=True)
        top_pos = semantic_sorted[:10]
        # noinspection PyTypeChecker
        semantic_sorted = sorted(semantic_orientation.items(), key=operator.itemgetter(1), reverse=False)
        top_neg = semantic_sorted[:10]
        print("\n\tThe 10 most positive terms in data.")
        print('\t' + str(top_pos) + '\n')
        print("\tThe 10 most negative terms in data.")
        print('\t' + str(top_neg))
    elif mode == 'term':
        if term in semantic_orientation:
            print("\n\tThe term '" + term + "' has a semantic orientation of " + str(semantic_orientation[term]))
        else:
            print("\nSorry, this term doesn't exist in the semantic dictionary.\n")
    elif mode == 'add':
        f_path = name[0] + "_SA_" + name[-2] + "_" + name[-1] + "." + ext
        f_out = open(f_path, 'wb')
        if not ext == 'json':
            with open(fname, 'r') as FILE:
                header = next(FILE).split(';')
                f_out.write(header[0] + ";" + header[1] + ";Subjectivity;" + header[-1])
                for line in FILE:
                    values = line.split(';')
                    text = values[-1].split()
                    subjectivity = 0
                    for word in text:
                        try:
                            subjectivity += semantic_orientation[word]
                        except KeyError:
                            continue
                    f_out.write("%s;%s;%s;%s\n" % (values[0], values[1], subjectivity, values[-1]))
        elif ext == 'json':
            with open(fname, 'r') as FILE:
                for line in FILE:
                    info = json.loads(line)
                    tweet = info['text'].encode('unicode_escape').split()
                    subjectivity = 0
                    for word in tweet:
                        try:
                            subjectivity += semantic_orientation[word]
                        except KeyError:
                            continue
                    twt = {"id": info['id'],
                           "created_at": info['created_at'],
                           "subjectivity": subjectivity,
                           "text": info['text']}
                    f_out.write(json.dumps(twt) + '\n')
        f_out.close()
    return
