import tweepy
import time
import private
import json
import dataset
from datetime import datetime
from sqlalchemy.exc import ProgrammingError
from textblob import TextBlob
from datafreeze import freeze
import logging
import boto3
from botocore.exceptions import ClientError

# --------------------------------- Initilization ----------------------------- #

csvFileName = "BD2020_" + str(datetime.now())

donnnyBoyTerms = ["Donald Trump", "Trump", "DonaldTrump"]

msLewinskyTerms = ["Joe Biden", "Biden", "JoeBiden"]

sqlTableName = csvFileName + "_table"

sqlConnectionString = "sqlite:///tweets.db"

db = dataset.connect(sqlConnectionString)

streamTimeLimit = 30


# --------------------------------- Stream Listener ----------------------------- #

class StreamListener(tweepy.StreamListener):

    def __init__(self, time_limit, term):
        self.start_time = time.time()
        self.limit = time_limit
        self.count = 0
        self.tracked_term = term
        super(StreamListener, self).__init__()

    # each time we get a tweet this method is called
    def on_status(self, status):
        self.count += 1
        if (time.time() - self.start_time) < self.limit and self.count < 50:

            # we dont care about retweets
            if status.retweeted:
                return

            # json fields returned that we chose to add to our database, can be adjusted later
            loc = status.user.location
            text = status.text
            name = status.user.screen_name
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweets = status.retweet_count
            blob = TextBlob(text)
            sent = blob.sentiment.polarity
            time_stamp = datetime.now()

            # need location since we are adding to a map
            if loc is None:
                return

            print("Tweet sent: " + str(sent))
            addItem(db, loc, text, name, followers, id_str, created, retweets, blob, sent, time_stamp)
            return True

        else:
            exportCSV(self.tracked_term)
            return False

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# -------------------------------------- Database Metzhods ----------------------------------- #

# Dataset is a lightweight database that lets us organzie/extract our stream data efficiently
def addItem(db, loc, text, name, followers, id_str, created, retweets, blob, sent, time_stamp):
    table = db[sqlTableName]
    try:
        table.insert(dict(
            user_location=loc,
            text=text,
            user_name=name,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
            polarity=sent,
            time=time_stamp
        ))
    except ProgrammingError as err:
        print(err)


# Method to write to unique csv file that we will later query
def exportCSV(canidateName):
    print("Export data to csv: " + canidateName + "_" + csvFileName)
    db = dataset.connect(sqlConnectionString)
    result = db[sqlTableName].all()
    newFileName = "data/" + canidateName + "_" + csvFileName + ".csv"
    freeze(result, format='csv', filename=newFileName)

    if canidateName == "B":
        bucket = "bd2020billtweets"
    else:
        bucket = "bd2020donaldtweets"
    upload_file(newFileName, bucket)


# -------------------------------------- AWS Metzhods ----------------------------------- #

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=private.AWS_ACCESS_KEY,
                             aws_secret_access_key=private.AWS_SECRET_KEY)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# ------------------------------------ Main -------------------------------- #

def main():
    # create instance of the listener
    auth = tweepy.OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
    auth.set_access_token(private.TWITTER_KEY, private.TWITTER_SECRET)
    api = tweepy.API(auth)
    print("Authorized with Twitter API")

    print("Streaming Trump tweets")
    stream_listener_Donny = StreamListener(streamTimeLimit, "D")
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener_Donny)
    stream.filter(track=donnnyBoyTerms)
    print("Streamed " + str(stream_listener_Donny.count) + " tweets")

    print("Streaming Biden tweets")
    stream_listener_Biden = StreamListener(streamTimeLimit, "B")
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener_Biden)
    stream.filter(track=msLewinskyTerms)
    print("Streamed " + str(stream_listener_Biden.count) + " tweets")


if __name__ == "__main__":
    main()