import tweepy
from textblob import TextBlob

key='XXX'
key_secret='XXX'
token='XXX'
token_secret='XXX'
auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token,token_secret)

api=tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
    	#analyze sentiment (contains subjectivity and polarity)
    	blob=TextBlob(status.text)
    	sent=blob.sentiment
    	polarity = sent.polarity
    	if(polarity<0.5):
    		sentiment="negative"
    	else:
    		sentiment="positive"
    	subjectivity = sent.subjectivity
    	print("sentiment: ", sentiment)
    	print("tweet: ", status.text)
    	#if(status.retweeted_status):
        	#return
        #if(not status.retweeted):
    def on_error(self, status_code):
        if status_code == 420:
            return False


#creating an nstance of the listener, designating the key words we are listening for
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["coronavirus", "rocket"])