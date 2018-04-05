################################
#         INTRODUCTION         #
################################

from langdetect import detect
from langdetect import lang_detect_exception

import pycountry
import json


############################
#         FUNCTION         #
############################

def basic_info(fname):
    with open(fname, 'r') as FILE:
        language_info = []
        total_num = 0
        coordinates_num = 0
        for line in FILE:
            tweet = json.loads(line)
            try:
                code = detect(tweet['text'])
            except lang_detect_exception.LangDetectException:
                continue
            if code in language_info:
                language_info[language_info.index(code) + 1] += 1
            else:
                language_info.append(code)
                language_info.append(1)
            try:
                if tweet['coordinates'] is not None:
                    coordinates_num += 1
            except KeyError:
                total_num += 1
                continue
            total_num += 1
        print("\tIn this collection, there is a total of " + str(total_num) + " tweets.")
        print("\tAlso, over all this tweets, there are " + str(coordinates_num) + " tweets with coordinates.")
        print("")
    for item in range(len(language_info)/2):
        try:
            language = pycountry.languages.get(alpha_2=language_info[item*2]).name
            print("\t - There are " + str(language_info[item*2 + 1]) + " tweets in " + language + ".")
        except KeyError:
            print("\t - There are " + str(language_info[item*2 + 1]) + " tweets in " + str(language_info[item*2]) + ".")
    return
