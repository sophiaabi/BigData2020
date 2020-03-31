# BigData2020
Insight on what is being tweeted about the political candidates in the 2020 election

Updates:

- Tweet stream data is now stored in a convienent csv file located under the data folder based on the time frame it was streamed
- StreamListener now has a time limit that can be changed in the initilization section of streaming_data.py
- Added main funciton that we can use once we put this thing on flask
- Added date and time fields for each tweet/database table so that we can sort for future use
- Added .gitignore so that we dont push meaningless/data sensitive files
- You will need to create your own private.py file for this to work and add it to the main directory (ask Thad for access keys)
- You will also need to download all the dependicies that we are using (pip3 install is perfect)

ToDo:

- Make this app available as a web application (using flask)
- Filter tweets via tracked term (not sure how to do this)
- Filter tweets via date 
- Create a map on the web application



Starting Flask App

  $ cd Flask_App

  $ . venv/bin/activate

  $ export FLASK_APP=app.py

  $ flask run
