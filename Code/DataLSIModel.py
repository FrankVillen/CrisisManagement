################################
#         INTRODUCTION         #
################################

from gensim import corpora, models, similarities
from six import iteritems
from DataClean import hexadecimal_conversion as hex_con
from DataClean import unicode_clean as uni_clc

import logging
import json
import os
import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


############################
#         FUNCTION         #
############################

def build_lsi_model(fname, topics, dname, terms, chunksize, directory):
    name = (fname.split(".")[0]).split("_")
    ext = fname.split(".")[1]
    dict_name = name[0] + "LSIDictionary_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".dict"
    f_name = name[0] + "LSIModel_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".txt"
    tfidf_name = name[0] + "TFIDFModel_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".tfidf"
    lsi_name = name[0] + "LSIModel_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".lsi"
    if dname == "default":
        if not ext == 'json':
            # Variables
            # ---------
            # @documents: the documents from we want create our dictionary
            # @prune_at: the number of terms of the dictionary. The preset is by default 2,000,000
            #
            # Collect statistics about all tokens/terms
            dictionary = corpora.Dictionary(documents=(line.split(";")[-1].split() for line in open(fname)),
                                            prune_at=terms)
        elif ext == 'json':
            # Variables
            # ---------
            # @documents: the documents from we want create our dictionary
            # @prune_at: the number of terms of the dictionary. The preset is by default 2,000,000
            #
            # Collect statistics about all tokens/terms
            dictionary = corpora.Dictionary(documents=(json.loads(line)['text'].encode('unicode_escape').split()
                                                       for line in open(fname)),
                                            prune_at=terms)
        wlr = open('WordListRemove.txt', 'r')
        word_list = set(str(wlr.readline()).split())
        wlr.close()
        # Find the specific words that we set
        word_ids = [dictionary.token2id[word_remove] for word_remove in word_list if word_remove in dictionary.token2id]
        # Find the words that appear only once
        once_ids = [token_id for token_id, doc_freq in iteritems(dictionary.dfs) if doc_freq == 1]
        # Remove specific words and words that appear only once
        dictionary.filter_tokens(word_ids + once_ids)
        # Remove gaps in id sequence after words that were removed
        dictionary.compactify()
    else:
        # If it is necessary, we can disable the limit of words in our dictionary at "prune_at". This is to save memory
        # on very large inputs. To disable this pruning, set 'prune_at=None'.
        dictionary = corpora.Dictionary(documents=(line.split() for line in open(dname)))
    # Store the dictionary, for future reference
    dictionary.save(directory + dict_name)
    # Other interesting commands:
    # print(dictionary)
    # print(dictionary.token2id)
    time.sleep(3)
    # It is possible to store the corpus to disk for later use. However, if we want to load it later, this means load
    # the whole corpus in the memory. So, if the corpus is really large, our computer will start an infinite loop
    # trying to read it unsuccessfully. Anyway, the code to do it is the next:
    #
    # # Store to disk, for later use
    # corpora.MmCorpus.serialize('directory/corpus_name.mm', MyCorpus())
    #
    # Another disadvantage is that the corpus stored will be really big, more or less like our original document.
    # To sump up, it is better to use the following code that it is memory friendly and don't overflow our memory
    # resources

    class MyCorpus(object):
        def __iter__(self):
            for line in open(fname):
                # Assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())
    # It is needed to transform our data, typically initialized by means of a 'training corpus'. Different
    # transformations may require different initialization parameters; in case of TfIdf, the "training" consists
    # simply of going through the supplied corpus once and computing document frequencies of all its features.
    # Training other models, such as Latent Semantic Analysis or Latent Dirichlet Allocation, is much more involved
    # and, consequently, takes much more time.
    #
    # Transformations always convert between two specific vector spaces. The same vector space must be used for
    # training as well as for subsequent vector transformations. Failure to use the same input feature space, such as
    # applying a different string preprocessing, using different feature ids, or using bag-of-words input vectors where
    # TfIdf vectors are expected, will result in feature mismatch during transformation calls and consequently in
    # either garbage output and/or runtime exceptions.
    tfidf = models.TfidfModel(MyCorpus())
    # Now, tfidf is treated as a read-only object that can be used to convert any vector from the old representation
    # to the new representation (TfIdf real-valued weights) or to apply a transformation to a whole corpus.
    corpus_tfidf = tfidf[MyCorpus()]
    # Variables
    # ---------
    # @corpus: it is the document we want to analyse
    # @id2word: is a mapping from word ids (integers) to words (strings). It is used to determine the vocabulary size,
    #           as well as for debugging and topic printing.
    # @num_topics: is the number of requested latent topics to be extracted from the training corpus.
    # @chunksize: the number of groups that we want to information be processed. The more groups we set, the faster
    #             will be our program. However, the more memory we will need. The size of `chunksize` is a tradeoff
    #             between increased speed (bigger `chunksize`) vs. lower memory footprint (smaller `chunksize`).
    #             If the distributed mode is on, each chunk is sent to a different worker/computer.
    #             The preset is by default in 20,000
    # @distributed: Turn on `distributed` to force distributed computing(see the `web tutorial
    #               <http://radimrehurek.com/gensim/distributed.html>` on how to set up a cluster of machines).
    #
    # The final model is stored as a matrix of num_terms x num_topics numbers. With 8 bytes per number
    # (double precision), that's 8 * num_terms * num_topics, i.e. for 100k terms in dictionary and 500 topics,
    # the model will be 8*100,000*500 = 400MB.
    #
    # That's just the output -- during the actual computation of this model, temporary copies are needed,
    # so in practice, you'll need about 3x that amount. For the 100k dictionary and 500 topics example,
    # you'll actually need ~1.2GB to create the LSI model.
    #
    # When out of memory, you'll have to either reduce the dictionary size or the number of topics (or add RAM!).
    # The memory footprint is not affected by the number of training documents, though.
    #
    # CONCLUSION: It is not exactly like this but it gives an idea about the variables that limit our model. One is
    # the number of TOPICS, the second is the terms in the DICTIONARY and the third is the number of CHUNKSIZE.
    #
    # Initialize an LSI transformation
    lsi = models.LsiModel(corpus=corpus_tfidf,
                          id2word=dictionary,
                          num_topics=topics,
                          chunksize=chunksize,
                          distributed=False)
    # Save the LSI Model and the Tfidf Model for later use
    lsi.save(directory + lsi_name)
    tfidf.save(directory + tfidf_name)
    # Others interesting commands:
    # lsi = models.LsiModel.load(directory + model_name)
    # lsi.print_topics(topics)
    lsi_str = str(lsi.print_topics(topics)).split('), (')
    f_model = open(f_name, 'wb')
    for line in lsi_str:
        f_model.write('{0}\n'.format(line.strip("[()]").replace("u'", "").replace("\"", "").replace("\'", "")))
    f_model.close()
    return


def analyse_lsi_model_topics(fname, ext, topics, lsi_model, directory):
    name = (fname.split(".")[0]).split("_")
    f_name = name[0] + "LSIModel_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".txt"
    classification_name = name[0] + "LSITopicsClassification_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ext
    tfidf_name = name[0] + "TFIDFModel_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".tfidf"
    dict_name = name[0] + "LSIDictionary_n" + str(topics) + "_" + name[-2] + "_" + name[-1] + ".dict"
    tfidf = models.TfidfModel.load(directory + tfidf_name)
    lsi = models.LsiModel.load(directory + lsi_model)
    dictionary = corpora.Dictionary.load(directory + dict_name)
    if os.path.isfile(classification_name):
        write = raw_input("\tThis archive exists. Do you want to rewrite the information? (y/n): ")
        if write == 'n':
            print("\nAccess denied.\n")
            return
    with open(classification_name, 'wb') as FILE:
        f_in = open(f_name, 'r')
        for number in range(topics):
            parameters = f_in.readline().split(',')
            FILE.write("TOPIC #" + str(number) + ";" + parameters[1].strip() + "\n")

    class MyCorpus(object):
        def __iter__(self):
            for line in open(fname):
                # Assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())
    # Create a double wrapper over the original corpus: bow -> tfidf -> fold-in-lsi
    corpus_lsi = lsi[tfidf[MyCorpus()]]
    # Both, bow -> tfidf and tfidf -> lsi transformations, are actually executed here, on the fly
    i = 1
    for doc in corpus_lsi:
        max_value = 0
        for thing in doc:
            if thing[1] < max_value:
                print(str(i) + ": " + str(thing))
        for item in doc:
            if abs(item[1]) >= max_value:
                max_value = abs(item[1])
        for num in doc:
            if abs(num[1]) == max_value:
                print(str(i) + ": " + str(num))
        print(doc)
        i += 1
        if i == 11:
            break
    return


def analyse_lsi_model_input(fname, topics, directory):
    # dict_name = (fname.split(".")[0]).replace('Preprocess', '') + "_n" + str(topics) + ".dict"
    corpus_name = (fname.split(".")[0]).replace('Preprocess', '') + "_n" + str(topics) + ".mm"
    index_name = (fname.split(".")[0]).replace('Preprocess', '') + "_n" + str(topics) + ".index"
    # f_name = "LSIModel" + (fname.split(".")[0]).replace('Preprocess', '') + "_n" + str(topics) + ".txt"
    model_name = "LSIModel" + (fname.split(".")[0]).replace('Preprocess', '') + "_n" + str(topics) + ".lsi"

    # dictionary = corpora.Dictionary.load(directory + dict_name)
    lsi = models.LsiModel.load(directory + model_name)
    corpus = corpora.MmCorpus(directory + corpus_name)

    # transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save(directory + index_name)
    # It is possible to load an index with the next code:
    # index = similarities.MatrixSimilarity.load(directory + index_name)
    #
    # This is true for all similarity indexing classes
    # - similarities.Similarity
    # - similarities.MatrixSimilarity
    # - similarities.SparseMatrixSimilarity)
    # Also in the following, index can be an object of any of these. When in doubt, use similarities.Similarity,
    # as it is the most scalable version, and it also supports adding more documents to the index later.


def word_list_remove():
    print("\n\tThis method modify the WordListRemove to erase determined expressions or word in the LSI Model.")
    wlr_name = 'WordListRemove.txt'
    new_words = []
    dictionary = []
    action = 1
    while action != 0:
        print("\t\t[1] Show the terms in the WordListRemove.")
        print("\t\t[2] Add a new term in the list.")
        print("\t\t[3] Remove a term in the list.")
        print("\t\t[4] Erase completely the list.")
        print("\t\t[0] Back to the LSI Model menu.\n")
        action = input("\t\tSelect an action: ")
        if action == 0:
            return
        elif action == 1:
            fname = open(wlr_name, 'r')
            dictionary = list(str(fname.readline()).split())
            fname.close()
            print("")
            i = 0
            for item in list(dictionary):
                i += 1
                print('\t\t\t' + str(i) + ': ' + item)
            print("")
        elif action == 2:
            with open(wlr_name, 'r') as FILE:
                for line in FILE:
                    for item in line.split():
                        dictionary.append(item)
            while True:
                print("\n\tIntroduce 0 if you want to stop or if you have finished.")
                term = uni_clc(hex_con(raw_input("\t\tAdd a term: ").decode('utf8').encode('unicode_escape')))
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
            with open(wlr_name, 'wb') as FILE:
                for item in dictionary:
                    FILE.write(item + " ")
        elif action == 3:
            with open(wlr_name, 'r') as FILE:
                for line in FILE:
                    for item in line.split():
                        dictionary.append(item)
            while True:
                print("\n\tIntroduce 0 if you want to stop or if you have finished.")
                term = uni_clc(hex_con(raw_input("\t\tAdd a term: ").decode('utf8').encode('unicode_escape')))
                if term == str(0):
                    break
            new_words.extend(term.lower().split())
            for item in new_words:
                dictionary.remove(item)
            with open(wlr_name, 'wb') as FILE:
                for item in dictionary:
                    FILE.write(item + " ")
        elif action == 4:
            fname = open(wlr_name, 'wb')
            fname.close()
