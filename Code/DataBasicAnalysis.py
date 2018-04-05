################################
#         INTRODUCTION         #
################################

from collections import defaultdict
from nltk import bigrams
from collections import Counter

import os.path
import pickle
import json
import operator
import DataClean as C


############################
#         FUNCTION         #
############################

def common_words(fname, call):
    name = fname.split('.')[0].split('_')
    count_name = name[0] + "WordsCounter_" + name[-2] + "_" + name[-1] + ".pkl"
    if not os.path.isfile(count_name):
        ext = fname.split('.')[1]
        wlr = open('WordListRemove.txt', 'r')
        word_list = list(wlr.readline().split())
        wlr.close()
        with open(fname, 'r') as FILE:
            count_all = Counter()
            if not ext == 'json':
                next(FILE)
                for line in FILE:
                    tweet = line.split(';')[len(line.split(';')) - 1]
                    # Create a list with all the terms
                    terms_stop = [term for term in tweet.split() if term not in word_list]
                    # Update the counter
                    count_all.update(terms_stop)
            elif ext == 'json':
                for line in FILE:
                    information = json.loads(line)
                    tweet = information['text'].encode('unicode_escape')
                    # Create a list with all the terms
                    terms_stop = [term for term in tweet.split() if term not in word_list]
                    # Update the counter
                    count_all.update(terms_stop)
        with open(count_name, 'wb') as FILE:
            pickle.dump(count_all, FILE)
    else:
        with open(count_name, 'r') as FILE:
            count_all = pickle.load(FILE)
    if call == 'print':
        # Print the first 5 most frequent words
        print("\n\tThe 5 most frequent words.")
        print("\t" + str(count_all.most_common(5)) + "\n")
        return count_all
    elif call == 'request information':
        return count_all
    else:
        print("\nInformation request not implemented.\n")
        return None


def common_hashtag(fname):
    ext = fname.split('.')[1]
    with open(fname, 'r') as FILE:
        count_has = Counter()
        if not ext == 'json':
            next(FILE)
            for line in FILE:
                tweet = C.unicode_clean(line.split(';')[len(line.split(';')) - 1])
                # Create a list with all the terms
                terms_has = [term for term in tweet.lower().split() if term.startswith('#')]
                # Update the counter
                count_has.update(terms_has)
        elif ext == 'json':
            for line in FILE:
                information = json.loads(line)
                tweet = C.unicode_clean(information['text'].encode('unicode_escape'))
                # Create a list with all the terms
                terms_has = [term for term in tweet.lower().split() if term.startswith('#')]
                # Update the counter
                count_has.update(terms_has)
    # Print the first 5 most frequent hashtag
    print("\n\tThe 5 most frequent hashtag.")
    print("\t" + str(count_has.most_common(5)) + "\n")
    return count_has


def common_pair_terms(fname):
    # The bigrams() function from NLTK will take a list of
    # tokens and produce a list of tuples using adjacent tokens.
    ext = fname.split('.')[1]
    wlr = open('WordListRemove.txt', 'r')
    word_list = list(wlr.readline().split())
    wlr.close()
    with open(fname, 'r') as FILE:
        count_bigrams = Counter()
        if not ext == 'json':
            next(FILE)
            for line in FILE:
                tweet = line.split(';')[len(line.split(';')) - 1]
                # Create a list with all the terms
                terms_bigram = bigrams([term for term in tweet.split() if term not in word_list])
                # Update the counter
                count_bigrams.update(terms_bigram)
        elif ext == 'json':
            for line in FILE:
                information = json.loads(line)
                tweet = information['text'].encode('unicode_escape')
                # Create a list with all the terms
                terms_bigram = bigrams([term for term in tweet.split() if term not in word_list])
                # Update the counter
                count_bigrams.update(terms_bigram)
    # Print the first 5 most frequent pair of words
    print("\n\tThe 5 most frequent pair of words.")
    print("\t" + str(count_bigrams.most_common(5)) + "\n")
    return count_bigrams


def common_co_occurrences(fname, call):
    name = fname.split('.')[0].split('_')
    dict_name = name[0] + "CoOccurrenceDictionary_" + name[-2] + "_" + name[-1] + ".json"
    com = defaultdict(lambda: defaultdict(int))
    if not os.path.isfile(dict_name):
        ext = fname.split('.')[1]
        wlr = open('WordListRemove.txt', 'r')
        word_list = list(wlr.readline().split())
        wlr.close()
        with open(fname, 'r') as FILE:
            if not ext == 'json':
                next(FILE)
                for line in FILE:
                    tweet = line.split(';')[len(line.split(';')) - 1]
                    terms_only = [term for term in tweet.split() if term not in word_list]
                    # Build co-occurrence matrix
                    for i in range(len(terms_only)-1):
                        for j in range(i+1, len(terms_only)):
                            w1, w2 = sorted([terms_only[i], terms_only[j]])
                            if w1 != w2:
                                com[w1][w2] += 1
            elif ext == 'json':
                for line in FILE:
                    information = json.loads(line)
                    tweet = information['text'].encode('unicode_escape')
                    terms_only = [term for term in tweet.split() if term not in word_list]
                    # Build co-occurrence matrix
                    for i in range(len(terms_only)-1):
                        for j in range(i+1, len(terms_only)):
                            w1, w2 = sorted([terms_only[i], terms_only[j]])
                            if w1 != w2:
                                com[w1][w2] += 1
        with open(dict_name, 'wb') as FILE:
            json.dump(com, FILE)
    else:
        with open(dict_name, 'r') as FILE:
            com.update(json.load(FILE))
    if call == 'print':
        com_max = []
        # For each term, look for the most common co-occurrence terms
        for t1 in com:
            t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        # Get the most frequent co-occurrences
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        print("\n\tThe 5 most frequent co-occurrence terms.")
        print("\t" + str(terms_max[:5]) + "\n")
        return terms_max
    elif call == 'request information':
        return com
    else:
        print("\nInformation request not implemented.\n")
        return None


def specific_co_occurrences(fname, search_word):
    ext = fname.split('.')[1]
    wlr = open('WordListRemove.txt', 'r')
    word_list = list(wlr.readline().split())
    wlr.close()
    count_search = Counter()
    with open(fname, 'r') as FILE:
        if not ext == 'json':
            next(FILE)
            for line in FILE:
                tweet = line.split(';')[len(line.split(';')) - 1]
                terms_only = [term for term in tweet.lower().split() if term not in word_list]
                if search_word in terms_only:
                    count_search.update(terms_only)
        elif ext == 'json':
            for line in FILE:
                information = json.loads(line)
                tweet = information['text'].encode('unicode_escape')
                terms_only = [term for term in tweet.lower().split() if term not in word_list]
                if search_word in terms_only:
                    count_search.update(terms_only)
    print("\n\tThe 5 most frequent co-occurrence terms for %s." % search_word)
    print("\t" + str(count_search.most_common(6)) + "\n")
    return count_search
