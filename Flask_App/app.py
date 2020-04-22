from flask import Flask, render_template
#from shelljob import proc
import csv

app = Flask(__name__)

@app.route('/')
def index():
    with open('/Users/Rocket/Desktop/BigData2020/data/B_BD2020_2020-04-21 21:24:19.572361.csv') as trump_csv_file:
        trump_data = csv.reader(trump_csv_file, delimiter=',')
        first_line = True
        trump_tweets = []
        for row in trump_data:
            if not first_line:
                trump_tweets.append({
                    "id": row[0],
                    "user_location": row[1],
                    "text": row[2]
                })
            else:
                first_line = False
        trump_csv_file.close()
# Bug: Under trump we get the trump tweets + the biden tweets at the end
#cont: Under biden we just get the trump tweets Need to fix this

    with open('/Users/Rocket/Desktop/BigData2020/data/D_BD2020_2020-04-21 21:24:19.572361.csv') as biden_csv_file:
        biden_data = csv.reader(biden_csv_file, delimiter=',')
        first_line1 = True
        biden_tweets = []
        for row in biden_data:
            if not first_line1:
                biden_tweets.append({
                    "id": row[0],
                    "user_location": row[1],
                    "text": row[2]
                })
            else:
                first_line1 = False
        biden_csv_file.close()

    return render_template('index.html', trump_tweets=trump_tweets, biden_tweets=biden_tweets)

