#!/bin/python3
print("Loading Modules")
import ijson
import mysql.connector
import datetime
import time

print ("Connecting to DB")
db = mysql.connector.connect(user='geolookup',password='redacted',host='localhost',database='geolookup')
cursor = db.cursor()

Records="../Takeout/Location History/Records.json" # path to records.json file

# for a complete record, we need timestamp, lat and lon
# latitudeE7,longitudeE7,timestamp
# 2010-12-14 10:16:49.030Z

count=0
datadict={}
tmpdata=[]
print("Opening json file: %s" % Records)
print("Iterating JSON")
for p,t,v in ijson.parse(open(Records)):
	count+=1
	if p=="locations.item.latitudeE7": datadict['latitude']=v
	if p=="locations.item.longitudeE7": datadict['longitude']=v
	if p=="locations.item.timestamp": datadict['timestamp']=v.replace('Z','')

	if 'latitude' in datadict and 'longitude' in datadict and 'timestamp' in datadict:
		#print (datadict)
		if count % 10 == 0:
			timedata=datadict['timestamp'].split('T')
			timestring="{} {}".format(timedata[0],timedata[1].split('.')[0])
			
			#print(datadict,timedata,timestring)
			tmpdata.append("('{}','{}','{}')".format(timestring,datadict['latitude'],datadict['longitude']) )
		if len(tmpdata) == 10000:
			tmpstring = ",".join(tmpdata)
			sql_cmd = "insert into history (timestamp, lat, lon) values {};".format(tmpstring)
			tmpdata=[]
			print("."),
			starttime=time.time()
			cursor.execute(sql_cmd)
			db.commit()
			endtime=time.time()
			print(f"Time taken: {endtime-starttime}")
		datadict={}
	# insert the last chunk of data
	if 'latitude' in datadict and 'longitude' in datadict and 'timestamp' in datadict:
		tmpstring=",".join(tmpdata)
		sql_cmd= "insert into history (timestamp, lat, lon) values {};".format(tmpstring)
		tmpdata=[]
		print("."),
		starttime=time.time()
		cursor.execute(sql_cmd)
		db.commit()
		endtime=time.time()
		print(f"Time taken: {endtime-starttime}")
	#print (p,t,v)
	#if count==100: break
