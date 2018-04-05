################################
#         INTRODUCTION         #
################################

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import tweepy
import time
import timeit
import string
import DataConfig
import os


############################
#         FUNCTION         #
############################

class MyListener(StreamListener):
    # Custom StreamListener for streaming data.
    def __init__(self, data_dir, query):
        super(MyListener, self).__init__()

        query_fname = format_filename(query)
        self.outfile = "%s/Stream%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        # If we want to execute the code for a specific time, the next 4 lines are the key
        global end
        if end != 0:
            if timeit.default_timer() - 0 > end:
                return False
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                # If we want to see all the data downloading, uncomment next line
                # print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(filename):
    """Convert file name into a safe string.
    Arguments:
        filename -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in filename)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


def start_stream(timing, query, directory_program):
    globals()['end'] = timing
    print("\n\tStarted at: " + time.strftime("%H:%M:%S"))
    authentic = OAuthHandler(DataConfig.consumer_key, DataConfig.consumer_secret)
    authentic.set_access_token(DataConfig.access_token, DataConfig.access_token_secret)
    # api = tweepy.API(authentic)
    tweets_stream = Stream(authentic, MyListener(data_dir=directory_program, query=query))
    tweets_stream.filter(track=[query])


###########################
#         PROGRAM         #
###########################

# Depends on the behaviour of our program, we can use this code for an infinite
# tweets acquisition or we can run it for a pre-set time on the DataProject

if __name__ == '__main__':
    print("***************************")
    print("*** PROJECT DATA STREAM ***")
    print("***************************\n")
    print("This tool allow you to acquire tweets that had been written in this moment.")
    print("If you want to collect tweets during a determinate period of time, use the DataProjectMainMenu.\n")
    end = 0
    directory = 'C:/Users/Fran/Documents/L3i/Tweets Analysis/Project Analysis/'
    term = raw_input("\tIntroduce the name of the query you want to stream: ").replace('#', '').capitalize()
    print("")
    if os.path.isfile("Stream" + term + ".json"):
        confirmation = raw_input("\tThis archive exists. Do you want to mixture the data? (y/n): ")
        print("")
        if confirmation == 'n':
            exit()
    print("\tStarted at: " + time.strftime("%H:%M:%S") + "\n")
    print("\tPress STOP bottom when you want to finish.")
    auth = OAuthHandler(DataConfig.consumer_key, DataConfig.consumer_secret)
    auth.set_access_token(DataConfig.access_token, DataConfig.access_token_secret)
    api = tweepy.API(auth)
    twitter_stream = Stream(auth, MyListener(data_dir=directory, query=term))
    twitter_stream.filter(track=[term])
