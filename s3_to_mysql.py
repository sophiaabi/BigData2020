import boto3
import pandas as pd
import private
from smart_open import smart_open
import mysql.connector
from mysql.connector import Error


#keep track of csv names that have already been read so we do not read them more than once
read_csv_b=[]
read_csv_t=[]

#dictionary to aid in extracting state-specific tweets from the S3 files
#form-   state abr:[list of all key words to look for (abr,full name, top 2 populus cities)]
state_info = {
    'AL': ['AL','Alabama','Montgomery','Birmingham'],
    'AK': ['AK','Alaska','Juneau','Anchorage'],
    'AZ': ['AZ','Arizona','Phoenix','Tuscon'],
    'AR': ['AR','Arkansas','Little Rock','Fayetteville'],
    'CA': ['CA','California','San Francisco','Los Angeles'],
    'CO': ['CO','Colorado','Denver','Colorado Springs'],
    'CT': ['CT','Connecticut','Hartford','Bridgeport'],
    'DE': ['DE','Delaware','Dover','Wilmington'],
    'FL': ['FL','Florida','Jacksonville','Miami'],
    'GA': ['GA','Georgia','Atlanta','Savannah'],
    'HI': ['HI','Hawaii','Honolulu','Oahu'],
    'ID': ['ID','Idaho','Boise','Meridian'],
    'IL': ['IL','Illinois','Springfield','Chicago'],
    'IN': ['IN','Indiana','Indianapolis','Fort Wayne'],
    'IA': ['IA','Iowa','Des Moines','Cedar Rapids'],
    'KS': ['KS','Kansas','Topeka','Wichita'],
    'KY': ['KY','Kentucky','Frankfort','Lexington'],
    'LA': ['LA','Louisiana','Baton Rouge','Jefferson County'],
    'ME': ['ME','Maine','Augusta','Lewiston'],
    'MD': ['MD','Maryland','Annapolis','Baltimore'],
    'MA': ['MA','Massachusetts','Boston','Worcester'],
    'MI': ['MI','Michigan','Lansing','Detroit'],
    'MN': ['MN','Minnesota','Saint Paul','Minneapolis'],
    'MS': ['MS','Mississippi','Jackson','Gulfport'],
    'MO': ['MO','Missouri','Jefferson City','St. Louis'],
    'MT': ['MT','Montana','Missoula','Billings'],
    'NE': ['NE','Nebraska','Lincoln','Omaha'],
    'NV': ['NV','Nevada','Las Vegas','Reno'],
    'NH': ['NH','New Hampshire','Concord','Manchester'],
    'NJ': ['NJ','New Jersey','Trenton','Newark'],
    'NM': ['NM','New Mexico','Santa Fe','Albuquerque'],
    'NY': ['NY','New York','Albany','Buffalo'],
    'NC': ['NC','North Carolina','Raleigh','Charlotte'],
    'ND': ['ND','North Dakota','Bismarck','Fargo'],
    'OH': ['OH','Ohio','Columbus','Cleveland'],
    'OK': ['OK','Oklahoma','Oklahoma City','Tulsa'],
    'OR': ['OR','Oregon','Salem','Portland'],
    'PA': ['PA','Pennsylvania','Pittsburgh','Philadelphia'],
    'RI': ['RI','Rhode Island','Providence','Warwick'],
    'SC': ['SC','South Carolina','Columbia','Charleston'],
    'SD': ['SD','South Dakota','Rapid City','Sioux Falls'],
    'TN': ['TN','Tennessee','Nashville','Memphis'],
    'TX': ['TX','Texas','Austin','Houston'],
    'UT': ['UT','Utah','Salt Lake City','Provo'],
    'VT': ['VT','Vermont','Montpelier','Burlington'],
    'VA': ['VA','Virginia','Richmond','Norfolk'],
    'WA': ['WA','Washington','Seattle','Spokane'],
    'WV': ['WV','West Virginia','Charleston','Huntington'],
    'WI': ['WI','Wisconsin','Madison','Milwaukee'],
    'WY': ['WY','Wyoming','Cheyenne','Casper']
}

#this dictionary will store [trump_total, trup_pos, trump_neg, biden_total, biden_pos, biden_neg] per state to be written to the database
state_totals={
	'AL': [0,0,0,0,0,0],
    'AK': [0,0,0,0,0,0],
    'AZ': [0,0,0,0,0,0],
    'AR': [0,0,0,0,0,0],
    'CA': [0,0,0,0,0,0],
    'CO': [0,0,0,0,0,0],
    'CT': [0,0,0,0,0,0],
    'DE': [0,0,0,0,0,0],
    'FL': [0,0,0,0,0,0],
    'GA': [0,0,0,0,0,0],
    'HI': [0,0,0,0,0,0],
    'ID': [0,0,0,0,0,0],
    'IL': [0,0,0,0,0,0],
    'IN': [0,0,0,0,0,0],
    'IA': [0,0,0,0,0,0],
    'KS': [0,0,0,0,0,0],
    'KY': [0,0,0,0,0,0],
    'LA': [0,0,0,0,0,0],
    'ME': [0,0,0,0,0,0],
    'MD': [0,0,0,0,0,0],
    'MA': [0,0,0,0,0,0],
    'MI': [0,0,0,0,0,0],
    'MN': [0,0,0,0,0,0],
    'MS': [0,0,0,0,0,0],
    'MO': [0,0,0,0,0,0],
    'MT': [0,0,0,0,0,0],
    'NE': [0,0,0,0,0,0],
    'NV': [0,0,0,0,0,0],
    'NH': [0,0,0,0,0,0],
    'NJ': [0,0,0,0,0,0],
    'NM': [0,0,0,0,0,0],
    'NY': [0,0,0,0,0,0],
    'NC': [0,0,0,0,0,0],
    'ND': [0,0,0,0,0,0],
    'OH': [0,0,0,0,0,0],
    'OK': [0,0,0,0,0,0],
    'OR': [0,0,0,0,0,0],
    'PA': [0,0,0,0,0,0],
    'RI': [0,0,0,0,0,0],
    'SC': [0,0,0,0,0,0],
    'SD': [0,0,0,0,0,0],
    'TN': [0,0,0,0,0,0],
    'TX': [0,0,0,0,0,0],
    'UT': [0,0,0,0,0,0],
    'VT': [0,0,0,0,0,0],
    'VA': [0,0,0,0,0,0],
    'WA': [0,0,0,0,0,0],
    'WV': [0,0,0,0,0,0],
    'WI': [0,0,0,0,0,0],
    'WY': [0,0,0,0,0,0]
}


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



#update total positive and negative numbers in database
def update_database():
	try:
		#connect to database
		connection=mysql.connector.connect(host='sql3.freemysqlhosting.net',database='sql3334934',user='sql3334934',password='jkBKdZYJFs')
		cursor=connection.cursor()

		#update candidate table for trump
		sql="""UPDATE Candidates SET positive = %s WHERE id = %s"""
		data=(total_pos_trump,1)
		cursor.execute(sql,data)
		sql="""UPDATE Candidates SET negative = %s WHERE id = %s"""
		data=(total_neg_trump,1)
		cursor.execute(sql,data)

		#update candidate table for biden
		sql="""UPDATE Candidates SET positive = %s WHERE id = %s"""
		data=(total_pos_biden,2)
		cursor.execute(sql,data)
		sql="""UPDATE Candidates SET negative = %s WHERE id = %s"""
		data=(total_neg_biden,2)
		cursor.execute(sql,data)

		#update location table
		for key,val in state_totals.items():
			sql="""UPDATE States SET Trump_Total=%s , Trump_Positive=%s , Trump_Negative=%s , Biden_Total=%s, Biden_Positive=%s, Biden_Negative=%s WHERE State_id=%s"""
			data=(val[0],val[1],val[2],val[3],val[4],val[5],key)
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
	global total_pos_biden
	global total_neg_biden
	for file in files_trump:
		filename=file.key.replace('data/','')
		if filename not in read_csv_t:
			read_csv_t.append(filename)
			df=pd.read_csv(smart_open(path_t+filename))
			df['user_location']=df['user_location'].astype(str)
			df['text']=df['text'].str.lower()
			#sum up positive and negative and update total
			bool_series_pos=df.apply(lambda x: True if (x['polarity']>0 and 'trump' in x['text'].lower()) else False, axis=1)
			bool_series_neg=df.apply(lambda x: True if (x['polarity']<0 and 'trump' in x['text'].lower()) else False, axis=1)

			total_pos_trump+=len(bool_series_pos[bool_series_pos==True].index)
			total_neg_trump+=len(bool_series_neg[bool_series_neg==True].index)
			print("positive count trump:",total_pos_trump)
			print("negative count trump:",total_neg_trump)

			bool_series_pos_b=df.apply(lambda x: True if (x['polarity']>0 and 'biden' in x['text'].lower()) else False, axis=1)
			bool_series_neg_b=df.apply(lambda x: True if (x['polarity']<0 and 'biden' in x['text'].lower()) else False, axis=1)

			total_pos_biden+=len(bool_series_pos_b[bool_series_pos_b==True].index)
			total_neg_biden+=len(bool_series_neg_b[bool_series_neg_b==True].index)
			print("positive count biden:",total_pos_biden)
			print("negative count biden:",total_neg_biden)

			for key,val in state_info.items():
				#trump tweets
				bool_loc_total=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and ('trump' in x['text'].lower())) else False, axis=1)
				bool_loc_pos=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']>0) and ('trump' in x['text'].lower())) else False, axis=1)
				bool_loc_neg=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']<0) and ('trump' in x['text'].lower())) else False, axis=1)

				state_totals[key][0]+=len(bool_loc_total[bool_loc_total==True].index)
				state_totals[key][1]+=len(bool_loc_pos[bool_loc_pos==True].index)
				state_totals[key][2]+=len(bool_loc_neg[bool_loc_neg==True].index)
				print("trump:",key,':',state_totals[key][0],state_totals[key][1],state_totals[key][2])

				#biden tweets
				bool_loc_total_b=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and ('biden' in x['text'].lower())) else False, axis=1)
				bool_loc_pos_b=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']>0) and ('biden' in x['text'].lower())) else False, axis=1)
				bool_loc_neg_b=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']<0) and ('biden' in x['text'].lower())) else False, axis=1)

				state_totals[key][3]+=len(bool_loc_total_b[bool_loc_total_b==True].index)
				state_totals[key][4]+=len(bool_loc_pos_b[bool_loc_pos_b==True].index)
				state_totals[key][5]+=len(bool_loc_neg_b[bool_loc_neg_b==True].index)
				print("biden:",key,':',state_totals[key][3],state_totals[key][4],state_totals[key][5])

def update_biden():
	global total_pos_biden
	global total_neg_biden
	global total_pos_trump
	global total_neg_trump
	for file in files_biden:
		filename=file.key.replace('data/','')
		if filename not in read_csv_b:
			read_csv_b.append(filename)
			df=pd.read_csv(smart_open(path_b+filename))
			#convert all locations to string (a few were floats and messing up the code)
			df['user_location']=df['user_location'].astype(str)
			df['text']=df['text'].str.lower()
			#sum up positive and negative and update total for biden
			bool_series_pos=df.apply(lambda x: True if ((x['polarity']>0) and ('biden' in x['text'].lower())) else False, axis=1)
			bool_series_neg=df.apply(lambda x: True if ((x['polarity']<0)  and ('biden' in x['text'].lower()))else False, axis=1)

			total_pos_biden+=len(bool_series_pos[bool_series_pos==True].index)
			total_neg_biden+=len(bool_series_neg[bool_series_neg==True].index)
			print("biden positive count:",total_pos_biden)
			print("biden negative count:",total_neg_biden)

			#total for trump
			bool_series_pos_t=df.apply(lambda x: True if (x['polarity']>0 and 'trump' in x['text'].lower()) else False, axis=1)
			bool_series_neg_t=df.apply(lambda x: True if (x['polarity']<0 and 'trump' in x['text'].lower()) else False, axis=1)

			total_pos_trump+=len(bool_series_pos_t[bool_series_pos_t==True].index)
			total_neg_trump+=len(bool_series_neg_t[bool_series_neg_t==True].index)
			print("positive count trump:",total_pos_trump)
			print("negative count trump:",total_neg_trump)
			for key,val in state_info.items():
				#biden
				bool_loc_total=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and ('biden' in x['text'].lower())) else False, axis=1)
				bool_loc_pos=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']>0) and ('biden' in x['text'].lower())) else False, axis=1)
				bool_loc_neg=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']<0) and ('biden' in x['text'].lower())) else False, axis=1)

				state_totals[key][3]+=len(bool_loc_total[bool_loc_total==True].index)
				state_totals[key][4]+=len(bool_loc_pos[bool_loc_pos==True].index)
				state_totals[key][5]+=len(bool_loc_neg[bool_loc_neg==True].index)
				print("biden:",key,':',state_totals[key][3],state_totals[key][4],state_totals[key][5])

				#trump
				bool_loc_total_t=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and ('trump' in x['text'].lower())) else False, axis=1)
				bool_loc_pos_t=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']>0) and ('trump' in x['text'].lower())) else False, axis=1)
				bool_loc_neg_t=df.apply(lambda x: True if ((val[0] in x['user_location'] or val[1] in x['user_location'] or val[2] in x['user_location'] or val[3] in x['user_location']) and (x['polarity']<0) and ('trump' in x['text'].lower())) else False, axis=1)

				state_totals[key][0]+=len(bool_loc_total_t[bool_loc_total_t==True].index)
				state_totals[key][1]+=len(bool_loc_pos_t[bool_loc_pos_t==True].index)
				state_totals[key][2]+=len(bool_loc_neg_t[bool_loc_neg_t==True].index)
				print("trump:",key,':',state_totals[key][0],state_totals[key][1],state_totals[key][2])
	


#need to put a timer on this to call these functions every 30 sec
update_trump()
update_biden()
update_database()
		