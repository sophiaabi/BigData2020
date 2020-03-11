import tweepy
import time
import private
import json
import dataset
from datetime import datetime 
from sqlalchemy.exc import ProgrammingError
from textblob import TextBlob
from datafreeze import freeze



# --------------------------------- Initilization ----------------------------- # 

csvFileName = "BD2020_" + str(datetime.now())

terms = ["Donald Trump", "Bernie Sanders",  "Bill Clinton"]

sqlTableName = csvFileName + "_table"

sqlConnectionString = "sqlite:///tweets.db"

db = dataset.connect(sqlConnectionString)

streamTimeLimit = 20



# --------------------------------- Stream Listener ----------------------------- # 

class StreamListener(tweepy.StreamListener):
	
	def __init__(self, time_limit=streamTimeLimit):
		self.start_time = time.time()
		self.limit = time_limit
		self.count = 0
		super(StreamListener, self).__init__()
	
	# each time we get a tweet this method is called
	def on_status(self, status):
		self.count +=1
		if (time.time() - self.start_time) < self.limit:

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
			sent = blob.sentiment
			time_stamp = datetime.now()

			# need location since we are adding to a map
			if loc is None:
				return

			# need positive tweets otherwise our data holds no significance
			if sent.polarity < 0:
				return

			print("Tweet from: " + str(loc))
			addItem(db, loc, text, name, followers, id_str, created, retweets, blob, sent,time_stamp)
			return True

		else:
			exportCSV()
			return False

		
	def on_error(self, status_code):
		if status_code == 420:
            #returning False in on_data disconnects the stream
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
			polarity=sent.polarity,
			subjectivity=sent.subjectivity,
			time = time_stamp
		))
	except ProgrammingError as err:
		print(err)

# Method to write to unique csv file that we will later query
def exportCSV():
	print("Export data to csv: " + csvFileName)
	db = dataset.connect(sqlConnectionString)
	result = db[sqlTableName].all()
	freeze(result, format='csv', filename= "data/" + csvFileName)


# ------------------------------------ Main -------------------------------- #

def main():

	# create instance of the listener
	auth = tweepy.OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
	auth.set_access_token(private.TWITTER_KEY, private.TWITTER_SECRET)
	api = tweepy.API(auth)
	print("Authorized with Twitter API")

	print("Streaming tweets")
	stream_listener = StreamListener()
	stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
	stream.filter(track = terms)
	print("Streamed " + str(stream_listener.count) + " tweets")
	

if __name__ == "__main__":
	main()