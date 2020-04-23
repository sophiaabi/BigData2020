import boto3
import pandas as pd
import private
from smart_open import smart_open
import mysql.connector
from mysql.connector import Error


#keep track of csv names that have already been read so we do not read them more than once
read_csv_b=[]
read_csv_t=[]

#global variables to hold total values for pos/neg tweets
total_pos_trump=0
total_neg_trump=0
total_pos_biden=0
total_neg_biden=0

s3=boto3.resource('s3',aws_access_key_id = private.AWS_ACCESS_KEY, aws_secret_access_key = private.AWS_SECRET_KEY)
client=boto3.client('s3',aws_access_key_id = private.AWS_ACCESS_KEY, aws_secret_access_key = private.AWS_SECRET_KEY)
bucket_b=s3.Bucket('bd2020bidentweets')
bucket_t=s3.Bucket('bd2020donaldtweets')

files_biden=bucket_b.objects.filter()
files_trump=bucket_t.objects.filter()

path_b='s3://bd2020bidentweets/data/'
path_t='s3://bd2020donaldtweets/data/'




def update_database(num_pos,num_neg,candidate_num):
	try:
		#connect to database
		connection=mysql.connector.connect(host='sql3.freemysqlhosting.net',database='sql3334934',user='sql3334934',password='jkBKdZYJFs')
		cursor=connection.cursor()

		#update
		sql="""UPDATE Candidates SET positive = %s WHERE id = %s"""
		data=(num_pos,candidate_num)
		cursor.execute(sql,data)
		sql="""UPDATE Candidates SET negative = %s WHERE id = %s"""
		data=(num_neg,candidate_num)
		cursor.execute(sql,data)
		#commit updates to database
		connection.commit()
		cursor.close()
		connection.close()
	except Error as error:
		print("ERROR:",error)
	


def update_trump():
	global total_pos_trump
	global total_neg_trump
	for file in files_trump:
		filename=file.key.replace('data/','')
		if filename not in read_csv_t:
			read_csv_t.append(filename)
			df=pd.read_csv(smart_open(path_t+filename))

			#sum up positive and negative and update total
			bool_series_pos=df.apply(lambda x: True if x['polarity']>0 else False, axis=1)
			bool_series_neg=df.apply(lambda x: True if x['polarity']<0 else False, axis=1)

			total_pos_trump+=len(bool_series_pos[bool_series_pos==True].index)
			total_neg_trump+=len(bool_series_neg[bool_series_neg==True].index)
			print("positive count:",total_pos_trump)
			print("negative count:",total_neg_trump)
	#after we loop thru all the new files, update databse with new numbers
	update_database(total_pos_trump,total_neg_trump,1)

def update_biden():
	global total_pos_biden
	global total_neg_biden
	for file in files_biden:
		filename=file.key.replace('data/','')
		if filename not in read_csv_b:
			read_csv_b.append(filename)
			df=pd.read_csv(smart_open(path_b+filename))

			#sum up positive and negative and update total
			bool_series_pos=df.apply(lambda x: True if x['polarity']>0 else False, axis=1)
			bool_series_neg=df.apply(lambda x: True if x['polarity']<0 else False, axis=1)

			total_pos_biden+=len(bool_series_pos[bool_series_pos==True].index)
			total_neg_biden+=len(bool_series_neg[bool_series_neg==True].index)
			print("positive count:",total_pos_biden)
			print("negative count:",total_neg_biden)
	#after we loop thru all the new files, update databse with new numbers
	update_database(total_pos_biden,total_neg_biden,2)


#need to put a timer on this to call these functions every 30 sec
update_trump()
update_biden()
		