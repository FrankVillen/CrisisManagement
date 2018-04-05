################################
#         INTRODUCTION         #
################################

from nltk.corpus import stopwords
from langdetect import detect
# Supports 55 languages out of the box ([ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes))
from langdetect import lang_detect_exception

import os
import string
import json
import DataClean as C
import preprocessor as p
import pycountry


############################
#         FUNCTION         #
############################

def first_step(directory, fname, ext, language):
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)
    os.chdir(directory)
    f_path = fname
    f_out_p = fname.split(".")[0].replace('Stream', '') + "Preprocess1" + language.upper() + "." + ext
    fo = open(f_out_p, 'wb')
    if not ext == 'json':
        fo.write("id;created_at;text" + "\n")
    with open(f_path, 'r') as FILE:
        next(FILE)
        i = 0
        for line in FILE:
            tweet = json.loads(line)
            if 'extended_tweet' in tweet:
                extended_tweet = tweet['extended_tweet']
                text = extended_tweet['full_text'].encode('unicode_escape')
            else:
                text = tweet['text'].encode('unicode_escape')
            try:
                if detect(text) == language.lower():
                    text = p.clean(text)
                    text = C.hexadecimal_conversion(text)
                    text = C.expression_clean(text)
                    if not ext == 'json':
                        fo.write("%s;%s;%s\n" % (i, tweet['created_at'], text))
                    elif ext == 'json':
                        twt = {"id": i,
                               "created_at": tweet['created_at'],
                               "text": text.decode('unicode_escape')}
                        fo.write(json.dumps(twt) + '\n')
                    i += 1
            except lang_detect_exception.LangDetectException:
                print("Lang Detect exception for: ", text)
    fo.close()
    return


def second_step(directory, fname, ext, language):
    os.chdir(directory)
    f_path = fname.split(".")[0] + "Preprocess1" + language.upper() + "." + ext
    f_out_p = fname.split(".")[0] + "Preprocess2" + language.upper() + "." + ext
    fo = open(f_out_p, 'wb')
    if not ext == 'json':
        fo.write("id;created_at;text\n")
        with open(f_path, 'r') as FILE:
            next(FILE)
            for line in FILE:
                values = line.split(';')
                text = C.unicode_clean(values[2])
                text = text.translate(None, string.punctuation).strip()
                text = text.replace('RT ', '')
                if text != '' and text is not None:
                    fo.write("%s;%s;%s\n" % (values[0], values[1], text))
    elif ext == 'json':
        with open(f_path, 'r') as FILE:
            for line in FILE:
                tweet = json.loads(line)
                text = tweet['text'].encode('unicode_escape')
                text = C.hexadecimal_conversion(text)
                text = C.unicode_clean(text)
                text = text.translate(None, string.punctuation).strip()
                text = text.replace('RT ', '')
                if text != '' and text is not None:
                    twt = {"id": tweet['id'],
                           "created_at": tweet['created_at'],
                           "text": text.decode('unicode_escape')}
                    fo.write(json.dumps(twt) + '\n')
    fo.close()
    return


def third_step(directory, fname, ext, language):
    os.chdir(directory)
    f_path = fname.split(".")[0] + "Preprocess2" + language.upper() + "." + ext
    f_out_p = fname.split(".")[0] + "Preprocess3" + language.upper() + "." + ext
    if not ext == 'json':
        fo = open(f_out_p, 'wb')
        fo.write("id;created_at;text\n")
        fo.close()
        with open(f_path, 'r') as FILE:
            next(FILE)
            for line in FILE:
                values = line.split(';')
                text = values[2]
                fo = open(f_out_p, 'r')
                write = 1
                for document in fo:
                    text_no_repeated = document.split(';')
                    if text_no_repeated[2] == text:
                        write = 0
                        break
                fo.close()
                if write == 1:
                    fo = open(f_out_p, 'a')
                    fo.write("%s;%s;%s" % (values[0], values[1], text))
                    fo.close()
    elif ext == 'json':
        fo = open(f_out_p, 'wb')
        fo.close()
        with open(f_path, 'r') as FILE:
            for line in FILE:
                tweet = json.loads(line)
                text = tweet['text'].encode('unicode_escape')
                fo = open(f_out_p, 'r')
                write = 1
                for document in fo:
                    twt_in = json.loads(document)
                    text_no_repeated = twt_in['text'].encode('unicode_escape')
                    if text_no_repeated == text:
                        write = 0
                        break
                fo.close()
                if write == 1:
                    fo = open(f_out_p, 'a')
                    twt = {"id": tweet['id'],
                           "created_at": tweet['created_at'],
                           "text": text.decode('unicode_escape')}
                    fo.write(json.dumps(twt) + '\n')
                    fo.close()
    return


def fourth_step(directory, fname, ext, language):
    os.chdir(directory)
    f_path = fname.split(".")[0] + "Preprocess2" + language.upper() + "." + ext
    f_out_p = fname.split(".")[0] + "_TR_" + language.upper() + "." + ext
    fo = open(f_out_p, 'wb')
    stop = stopwords.words(pycountry.languages.get(alpha_2=language.lower()).name)
    if not ext == 'json':
        fo.write("id;created_at;text\n")
        with open(f_path, 'r') as FILE:
            next(FILE)
            for line in FILE:
                values = line.split(';')
                text = values[2].lower()
                for word in stop:
                    search = " " + word + " "
                    replace = " "
                    text = text.replace(search, replace)
                fo.write("%s;%s;%s" % (values[0], values[1], text))
    elif ext == 'json':
        with open(f_path, 'r') as FILE:
            for line in FILE:
                tweet = json.loads(line)
                text = tweet['text'].encode('unicode_escape').lower()
                for word in stop:
                    search = " " + word + " "
                    replace = " "
                    text = text.replace(search, replace)
                twt = {"id": tweet['id'],
                       "created_at": tweet['created_at'],
                       "text": text.decode('unicode_escape')}
                fo.write(json.dumps(twt) + '\n')
    fo.close()
    if os.path.isfile(fname.split(".")[0] + "Preprocess3" + language.upper() + "." + ext):
        f_path = fname.split(".")[0] + "Preprocess3" + language.upper() + "." + ext
        f_out_p = fname.split(".")[0] + "_TNR_" + language.upper() + "." + ext
        fo = open(f_out_p, 'wb')
        if not ext == 'json':
            fo.write("id;created_at;text\n")
            with open(f_path, 'r') as FILE:
                next(FILE)
                for line in FILE:
                    values = line.split(';')
                    text = values[2].lower()
                    for word in stop:
                        search = " " + word + " "
                        replace = " "
                        text = text.replace(search, replace)
                    fo.write("%s;%s;%s" % (values[0], values[1], text))
        elif ext == 'json':
            with open(f_path, 'r') as FILE:
                for line in FILE:
                    tweet = json.loads(line)
                    text = tweet['text'].encode('unicode_escape').lower()
                    for word in stop:
                        search = " " + word + " "
                        replace = " "
                        text = text.replace(search, replace)
                    twt = {"id": tweet['id'],
                           "created_at": tweet['created_at'],
                           "text": text.decode('unicode_escape')}
                    fo.write(json.dumps(twt) + '\n')
        fo.close()
    return
