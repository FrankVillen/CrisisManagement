################################
#         INTRODUCTION         #
################################

import DataStream
import DataInformation
import DataPreprocessing
import DataBasicAnalysis
import DataBasicVisualisation
import DataSubjectiveAnalysis
import DataLSIModel
import os
import time


#############################
#         VARIABLES         #
#############################

directory = 'C:/Users/Fran/Documents/L3i/Tweets Analysis/Project Analysis/'


############################
#         FUNCTION         #
############################

def stream():
    print("Stream Menu")
    print("-----------\n")
    print("\tIntroduce the time in seconds you want to be streaming.")
    print("\tIntroduce 0 if you want to back to main menu.\n")
    timing = input("\t\tTime (s): ")
    if timing == 0:
        print("")
        return
    elif timing > 0:
        query = raw_input("\t\tIntroduce the query you want to stream: ").replace('#', '').capitalize()
        if os.path.isfile("Stream" + query + ".json"):
            confirmation = raw_input("\t\tThis archive exists. Do you want to mixture the data? (y/n): ")
            print("")
            if confirmation == 'n':
                return
        DataStream.start_stream(timing=timing,
                                query=query,
                                directory_program=directory)
        print("\tFinished at: " + time.strftime("%H:%M:%S"))
        print("\nAction finished.\n")
    else:
        print("\nError with the value introduced.\n")
    return


def information():
    while True:
        print("Information Menu")
        print("----------------\n")
        print("\tIntroduce the name of the file with the Data stored.")
        print("\tIntroduce 0 if you want to back to main menu.\n")
        fname = raw_input("\t\tIntroduce the name of the original json file: ")
        print("")
        if fname == str(0):
            return
        elif os.path.isfile(fname):
            DataInformation.basic_info(fname=fname)
            print("\nAction finished.\n")
        else:
            print("\nSorry, file hasn't found.\n")


def preprocess():
    while True:
        print("Pre-process Menu")
        print("----------------\n")
        print("\tIntroduce the name of the file with the Data stored.")
        print("\tIntroduce 0 if you want to back to main menu.\n")
        fname = raw_input("\t\tIntroduce the name of the original json file: ")
        if fname == str(0):
            print("")
            return
        elif os.path.isfile(fname):
            ext = raw_input("\t\tIntroduced the extension of the output file (csv, txt, json): ")
            language = raw_input("\t\tIntroduced the code of the language (en, fr, es, de, zh, ja): ")
            no_repeated = raw_input("\t\tDo you want to store the no repeated tweets? (y/n): ")
            print("")
            # With the aim of get a shorter name, we will erase the word 'Stream'. However, we
            # need the original name in the first step.
            DataPreprocessing.first_step(directory=directory,
                                         fname=fname,
                                         ext=ext,
                                         language=language)
            fname = fname.replace('Stream', '')
            DataPreprocessing.second_step(directory=directory,
                                          fname=fname,
                                          ext=ext,
                                          language=language)
            if no_repeated == "y":
                DataPreprocessing.third_step(directory=directory,
                                             fname=fname,
                                             ext=ext,
                                             language=language)
            DataPreprocessing.fourth_step(directory=directory,
                                          fname=fname,
                                          ext=ext,
                                          language=language)
            print("\nAction finished.\n")
        else:
            print("\nSorry, file hasn't found.\n")


def basic_analysis():
    basic_action = 1
    while basic_action != 0:
        print("Basic Analysis Menu")
        print("-------------------\n")
        print("\t[1] The most 5 common words in Data.")
        print("\t[2] The most 5 common hashtag in Data.")
        print("\t[3] The most 5 common pair of words in Data.")
        print("\t[4] The most 5 frequent co-occurrence terms in Data.")
        print("\t[5] The most 5 frequent specific co-occurrence terms in Data.")
        print("\t[0] Back to the main menu.\n")
        basic_action = input("\tSelect an action: ")
        if basic_action == 0:
            print("")
        elif basic_action == 1:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_words(fname=fname,
                                                         call='print')
                DataBasicVisualisation.bar_plot(fname=fname,
                                                count_all=counter,
                                                at="CommonWords",
                                                term="")
                print("File Bar generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif basic_action == 2:
            fname = raw_input("\tIntroduce the name of the file Preprocess1: ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_hashtag(fname)
                DataBasicVisualisation.bar_plot(fname=fname,
                                                count_all=counter,
                                                at="CommonHashtag",
                                                term="")
                print("File Bar generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif basic_action == 3:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_pair_terms(fname=fname)
                DataBasicVisualisation.bar_plot(fname=fname,
                                                count_all=counter,
                                                at="PairWords",
                                                term="")
                print("File Bar generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif basic_action == 4:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_co_occurrences(fname=fname,
                                                                  call='print')
                DataBasicVisualisation.bar_plot(fname=fname,
                                                count_all=counter,
                                                at="CommonCoOccurrences",
                                                term="")
                print("File Bar generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif basic_action == 5:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                term = raw_input("\tIntroduce the term to analyse the co-occurrence: ")
                counter = DataBasicAnalysis.specific_co_occurrences(fname=fname,
                                                                    search_word=term)
                DataBasicVisualisation.bar_plot(fname=fname,
                                                count_all=counter,
                                                at="SpecificCoOccurrences",
                                                term=term)
                print("File Bar generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        else:
            print("\nAction not implemented yet.\n")
    return


def visual_analysis():
    visual_action = 1
    while visual_action != 0:
        print("Visual Analysis Menu")
        print("--------------------\n")
        print("\t[1] Observe the distribution of a term in tweets over the time.")
        print("\t[2] Observe the distribution of tweets over the map.")
        print("\t[0] Back to the main menu.\n")
        visual_action = input("\tSelect an action: ")
        if visual_action == 0:
            print("")
        elif visual_action == 1:
            fname = raw_input("\tIntroduce the name of the file Preprocess1: ")
            if os.path.isfile(fname):
                term = raw_input("\tIntroduce the term you want to study: ")
                # resample('1/1/2011', periods=72, freq='H') --> 72 hours starting with midnight Jan 1st, 2011
                # 'D' re-sample by day
                # 'T' or 'noMin' re-sample by minutes
                print("\n\tSet the time intervals: '1T' -> one minute")
                print("\t                        '1H' -> one hour")
                print("\t                        '1D' -> one day")
                print("\t                        '1M' -> one month")
                print("\t                        '1Y' -> one year")
                print("\tIf you need specify more the time intervals, modify it at the function (help at comments).\n")
                classified = raw_input("\tIntroduce how the time intervals are going to be: ")
                DataBasicVisualisation.time_plot(fname=fname,
                                                 search_word=term,
                                                 classified=classified)
                print("\nFile Time generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif visual_action == 2:
            fname = raw_input("\tIntroduce the name of the original json file: ")
            if os.path.isfile(fname):
                DataBasicVisualisation.map_plot(fname=fname,
                                                directory=directory)
                print("\nFile Map generated. Check in the folder and open it in PyCharm.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        else:
            print("\nAction not implemented yet.\n")
    return


def sentimental_analysis():
    sentimental_action = 1
    while sentimental_action != 0:
        print("Subjectivity Analysis Menu")
        print("--------------------------\n")
        print("\t[1] Print the positive terms of the sentimental dictionary.")
        print("\t[2] Print the negative terms of the sentimental dictionary.")
        print("\t[3] Build a new sentimental dictionary or translate to other language.")
        print("\t[4] Calculate the most 10 positive and negative terms in the data.")
        print("\t[5] Calculate the subjectivity of a specific term.")
        print("\t[6] Calculate the subjectivity of each tweet.")
        print("\t[0] Back to the main menu.\n")
        sentimental_action = input("\tSelect an action: ")
        if sentimental_action == 0:
            print("")
        elif sentimental_action == 1:
            print("\tWhich language you want to print the dictionary.")
            language = raw_input("\tIntroduced the code of the language (en, fr, es, de, zh, ja): ")
            fname = 'PositiveWords_' + language.upper() + '.txt'
            if os.path.isfile(fname):
                DataSubjectiveAnalysis.print_dictionary(language=language,
                                                        part=fname,
                                                        sign='Positive')
                print("\nAction finished.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif sentimental_action == 2:
            print("\tWhich language you want to print the dictionary.")
            language = raw_input("\tIntroduced the code of the language (en, fr, es, de, zh, ja): ")
            fname = 'NegativeWords_' + language.upper() + '.txt'
            if os.path.isfile(fname):
                DataSubjectiveAnalysis.print_dictionary(language=language,
                                                        part=fname,
                                                        sign='Negative')
                print("\nAction finished.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif sentimental_action == 3:
            create = raw_input("\tAre you going to create a new dictionary? (y/n): ")
            if create == 'y':
                fname = raw_input("\tIntroduce the name of the dictionary (with extension): ")
                if os.path.isfile(fname):
                    write = raw_input("\tThis archive exists. Do you want to mixture the information? (y/n): ")
                    if write == 'y':
                        DataSubjectiveAnalysis.new_dictionary(help=None,
                                                              part=fname)
                        print("\nDictionary saved.\n")
                    else:
                        print("\nAccess denied.\n")
                else:
                    DataSubjectiveAnalysis.new_dictionary(help=None,
                                                          part=fname)
                    print("\nDictionary saved.\n")
            elif create == 'n':
                translate = raw_input("\tAre you going to translate the positive dictionary? (y/n): ")
                print("\tWhich language you are going to translate the dictionary.")
                language = raw_input("\tIntroduced the code of the language (en, fr, es, de, zh, ja): ")
                if translate == 'y':
                    fname = 'PositiveWords_' + language.upper() + '.txt'
                    if os.path.isfile(fname):
                        write = raw_input("\tThis archive exists. Do you want to mixture the information? (y/n): ")
                        if write == 'y':
                            DataSubjectiveAnalysis.new_dictionary(help='PositiveWords_EN.txt',
                                                                  part=fname)
                            print("\nDictionary saved.\n")
                        else:
                            print("\nAccess denied.\n")
                    else:
                        DataSubjectiveAnalysis.new_dictionary(help='PositiveWords_EN.txt',
                                                              part=fname)
                        print("\nDictionary saved.\n")
                elif translate == 'n':
                    fname = 'NegativeWords_' + language.upper() + '.txt'
                    if os.path.isfile(fname):
                        write = raw_input("\tThis archive exists. Do you want to mixture the information? (y/n): ")
                        if write == 'y':
                            DataSubjectiveAnalysis.new_dictionary(help='NegativeWords_EN.txt',
                                                                  part=fname)
                            print("\nDictionary saved.\n")
                        else:
                            print("\nAccess denied.\n")
                    else:
                        DataSubjectiveAnalysis.new_dictionary(help='NegativeWords_EN.txt',
                                                              part=fname)
                        print("\nDictionary saved.\n")
                else:
                    print("\nPlease, answer yes (y) or no (n).\n")
            else:
                print("\nPlease, answer yes (y) or no (n).\n")
        elif sentimental_action == 4:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_words(fname=fname,
                                                         call='request information')
                com = DataBasicAnalysis.common_co_occurrences(fname=fname,
                                                              call='request information')
                language = fname.split('.')[0][-2:]
                DataSubjectiveAnalysis.subjective_analysis(fname=fname,
                                                           terms_tweets=counter,
                                                           com=com,
                                                           language=language,
                                                           mode='10th',
                                                           term=None)
                print("\nAction finished.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif sentimental_action == 5:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_words(fname=fname,
                                                         call='request information')
                com = DataBasicAnalysis.common_co_occurrences(fname=fname,
                                                              call='request information')
                language = fname.split('.')[0][-2:]
                term = raw_input("\tIntroduce the term you want to study: ").lower()
                DataSubjectiveAnalysis.subjective_analysis(fname=fname,
                                                           terms_tweets=counter,
                                                           com=com,
                                                           language=language,
                                                           mode='term',
                                                           term=term)
                print("\nAction finished.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif sentimental_action == 6:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                counter = DataBasicAnalysis.common_words(fname=fname,
                                                         call='request information')
                com = DataBasicAnalysis.common_co_occurrences(fname=fname,
                                                              call='request information')
                language = fname.split('.')[0][-2:]
                DataSubjectiveAnalysis.subjective_analysis(fname=fname,
                                                           terms_tweets=counter,
                                                           com=com,
                                                           language=language,
                                                           mode='add',
                                                           term=None)
                print("\nAction finished.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        else:
            print("\nAction not implemented yet.\n")
    return


def lsi_models():
    lsi_action = 1
    dictionary = "default"
    while lsi_action != 0:
        print("LSI Model Menu")
        print("--------------\n")
        print("\t[1] Build a LSI Model.")
        print("\t[2] Calculates similarities between tweets and topics from a LSI Model.")
        print("\t[3] Calculates similarities between tweets and an input.")
        print("\t[4] Modify the Word List Remove.")
        print("\t[5] Select a specific dictionary.")
        print("\t[0] Back to the main menu.\n")
        lsi_action = input("\tSelect an action: ")
        if lsi_action == 0:
            print("")
        elif lsi_action == 1:
            print("\n\tThis action may take a while depending on the large of the data.")
            print("\tDepending on the results you want to achieve, you need to modify:")
            print("\t - The WordListRemove in the other method.")
            print("\t - The number of Topics.")
            print("\t - The number of terms in the default Dictionary (The preset value is 2 000 000).")
            print("\t - The number of Chunksize (The preset value is 20 000).\n")
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                n_topics = input("\tIntroduce the number of topics: ")
                if dictionary == "default":
                    n_terms = input("\tIntroduce the number of terms in the default dictionary: ")
                else:
                    n_terms = 2000000
                n_chunksize = input("\tIntroduce the number of chunksize: ")
                print("")
                DataLSIModel.build_lsi_model(fname=fname,
                                             topics=n_topics,
                                             dname=dictionary,
                                             terms=n_terms,
                                             chunksize=n_chunksize,
                                             directory=directory)
                time.sleep(3)
                print("\nLSI Model created.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif lsi_action == 2:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            if os.path.isfile(fname):
                n_topics = input("\tIntroduce the number of topics the model has been created: ")
                ext = raw_input("\tIntroduce the file extension of the results (csv, txt, json): ")
                ext = '.' + ext
                name = (fname.split(".")[0]).split("_")
                lsi = name[0] + "LSIModel_n" + str(n_topics) + "_" + name[-2] + "_" + name[-1] + ".lsi"
                if os.path.isfile(lsi):
                    DataLSIModel.analyse_lsi_model_topics(fname=fname,
                                                          ext=ext,
                                                          topics=n_topics,
                                                          lsi_model=lsi,
                                                          directory=directory)
                    print("\nAction finished.\n")
                else:
                    print("\nSorry, this specific model hadn't been found.\n")
            else:
                print("\nSorry, file hasn't found.\n")
        elif lsi_action == 3:
            fname = raw_input("\tIntroduce the name of the final file (TR or TNR): ")
            # Buscar si esta el modelo hecho --> Es decir, construir el formato del nombre del modelo
            if os.path.isfile(fname):
                print("Building")
        elif lsi_action == 4:
            DataLSIModel.word_list_remove()
            print("\nAction finished.\n")
        elif lsi_action == 5:
            print("\n\tSelect a dictionary to build the LSI Model.")
            print("\tIf you want to build a dictionary from the data, just set it as \"default\".\n")
            name = raw_input("\tIntroduce the name of the dictionary: ")
            if os.path.isfile(name):
                dictionary = name
                print("\nAction finished.\n")
            else:
                print("\nSorry, file haven't found.\n")
        else:
            print("\nAction not implemented yet.\n")


def lda_models():
    print("Building")
    print("")


def w2v_models():
    print("Building")
    print("")


###########################
#         PROGRAM         #
###########################

if __name__ == '__main__':
    print("*****************************")
    print("*** PROJECT DATA ANALYSIS ***")
    print("*****************************\n")
    action = 1
    while action != 0:
        print("Main Menu")
        print("---------\n")
        print("\t[1] Stream Data from Twitter.")
        print("\t[2] Information about the acquired Data.")
        print("\t[3] Preprocess the acquired Data.")
        print("\t[4] Basic Analysis from Data.")
        print("\t[5] Visual Analysis from Data.")
        print("\t[6] Sentimental and Subjectivity Analysis from Data.")
        print("\t[7] LSI Model Analysis.")
        print("\t[8] LDA Model Analysis.")
        print("\t[9] Word2Vec Model Analysis.")
        print("\t[0] Finish and close the program.\n")
        action = input("\tSelect an action: ")
        print("")
        if action == 0:
            continue
        elif action == 1:
            stream()
        elif action == 2:
            information()
        elif action == 3:
            preprocess()
        elif action == 4:
            basic_analysis()
        elif action == 5:
            visual_analysis()
        elif action == 6:
            sentimental_analysis()
        elif action == 7:
            lsi_models()
        elif action == 8:
            lda_models()
        elif action == 9:
            w2v_models()
        elif action > 9 or action < 0:
            print("Action not implemented yet.\n")
    print("Closing Program. Bye.")
