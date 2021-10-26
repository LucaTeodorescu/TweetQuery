import os
import pandas as pd
import PySimpleGUI as sg
from threading import Thread
from snscrape.modules.twitter import TwitterSearchScraper

class TweetQuery:

    def __init__(self):
        sg.theme("DarkAmber")
        self.window = None
        self.layout = [
        [sg.Text("Enter text to fetch : "), sg.InputText(key = "-TEXT-"), sg.Text("add # before to search for hastags")],
        [sg.Text("Since.. Until.. (optional)"), sg.InputText(key = "-SINCE-"), sg.InputText(key = "-UNTIL-"), sg.Text("format : YYYY-MM-DD")],
        [sg.Text("File Name : "), sg.InputText(key = "-FILENAME-"), sg.Text("eg : 'Tweets' to get 'Tweets.csv'")],
        [sg.Button("Query", key = "query"), sg.Text("", key = "loading", size = (105,1)), sg.Button("Done", key = "exit")]
        ]



    def run(self):

        self.window = sg.Window("Tweet Query", layout = self.layout)

        self.window.read(timeout = 1)

        while True:
            event, valuesread = self.window.read(timeout = 33)
            if event == sg.WIN_CLOSED or event == "exit":
                self.window.close()
                break
            elif event == "query":
                self.query(valuesread)
            elif event != "__TIMEOUT__":
                print(event, valuesread)

    def text_query(self, text, since = "", until = "", tweet_count = "", file_name = "text_query"):
        if since == "":
            since_tx = ""
        else :
            since_tx = "since:{} ".format(since)
        if until == "":
            until_tx = ""
        else :
            until_tx = "until:{}".format(until)


        """os.system('snscrape {}{}twitter-search "{}{}"> datas\{}.txt'.format(tweet_count_tx, since_tx, text, until_tx, file_name))
        with open('datas\{}.txt'.format(file_name)) as f:
            lines = f.readlines()"""

        tweets_list = []
        for i,tweet in enumerate(TwitterSearchScraper('{} {}{}'.format(text, since_tx, until_tx)).get_items()):
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.retweetCount, tweet.quoteCount, tweet.likeCount, tweet.replyCount])

        dftweets = pd.DataFrame(tweets_list, columns = ['Datetime', 'Tweet ID', 'Text', 'Username', 'Number of Retweets', 'Number of Quotes', 'Nummber of Likes', 'Nummber of Replies'])

        dftweets.to_csv('datas\{}.csv'.format(file_name))
        self.window["loading"](value="Done!, {} tweets loaded.".format(str(len(dftweets.index))))
        return dftweets

    def query(self,valuesread):
        self.window["loading"](value="Fetching...")
        Thread(target=self.text_query, args=(valuesread["-TEXT-"],), kwargs = {"since" : valuesread["-SINCE-"], "until" : valuesread["-UNTIL-"], "file_name" : valuesread["-FILENAME-"]}).start()

"""TweetQuery().run()"""
