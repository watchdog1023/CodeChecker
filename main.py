#!/usr/bin/python3
from sys import byteorder
from array import array
from struct import pack

import sys
import speech_recognition as sr
import mysql.connector
import pyaudio
import wave
import os
import subprocess
import acoustid
import chromaprint

username = "project"
password = "root"
dbname2 = "song_base"
dbhost = "192.168.1.110"

def db_connect(search,fallback333 = 0):
	fallback = 0
	fallbackp = fallback333[0:7]
	fallback = float(fallbackp)
	print(fallback)
	mydb = mysql.connector.connect(host = dbhost,user = username,passwd = password,database = dbname2)
	mycursor = mydb.cursor()
	sql = "SELECT * FROM song_table WHERE Fingerprint = " + "\"" + search + "\""
	mycursor.execute(sql)
	myresult = mycursor.fetchone()
	if myresult:
		print(myresult[1])
	else:
		#print("Nothing Found")
		sql = "SELECT * FROM song_table WHERE Fingerprint like " + "\'" + search + "%\'"
		mycursor.execute(sql)
		myresult2 = mycursor.fetchone()
		if myresult2:
			print(myresult2[1])
		else:
			#print("Nothing found")
			sql = "SELECT * FROM song_table WHERE Fingerprint like " + "\'%" + search + "\'"
			mycursor.execute(sql)
			myresult3 = mycursor.fetchone()
			if myresult3:
				print(myresult3[1])
			else:
				#print("Nothing found")
				sql = "SELECT * FROM song_table WHERE Fingerprint like " + "\'%" + search + "%\'"
				mycursor.execute(sql)
				myresult4 = mycursor.fetchone()
				if myresult4:
					print(myresult4[1])
				else:
					#print("Nothing found")
					print("Starting fallback search method")
					print(fallback)
					sql = "SELECT * FROM song_table WHERE BPM like " + "\"" + str(fallback) + "\""
					mycursor.execute(sql)
					myresultf = mycursor.fetchone()
					if myresultf:
						print(myresultf[1])
					else:
						print("Nothing Found BPM")
						fallback2 = 0
						fallback = fallback + 1
						fallback2 = int(fallback)
						print(fallback)
						sql = "SELECT * FROM song_table WHERE BPM like " + "\"" + str(fallback2) + "\""
						mycursor.execute(sql)
						myresultf2 = mycursor.fetchone()
						if myresultf2:
							print(myresultf2[1])
						else:
							print("Nothing Found BPM")
							fallback3 = 0
					#		fallback =- 2
					#		fallback3 = fallback
							print(fallback)
							sql = "SELECT * FROM song_table WHERE BPM like " + "\"" + str(fallback3) + "\""
							mycursor.execute(sql)
							myresultf3 = mycursor.fetchone()
							if myresultf3:
								print(myresultf3[1])
							else:
								print("Nothing Found BPM")


def update_db(dbname,dbfingerprint,dbbpm,dblyrics):
    mydb = mysql.connector.connect(host = dbhost,user = username,passwd = password,database = dbname2)
    mycursor = mydb.cursor()
    sql = "INSERT INTO song_table (name, BPM, Lyric, Fingerprint) VALUES ("+ "\"" + str(dbname) + "\""  + ", " + "\"" + dbbpm + "\"" + ", " + "\""+str(dblyrics)+"\"" + ", " +"\""+ dbfingerprint+"\"" + ")"
    mycursor.execute(sql)
    mydb.commit()
    print("1 record inserted, ID:", mycursor.lastrowid)

def get_bpm(filename_m):
	batcmd = "aubio tempo " + "\"" + filename_m + "\""
	result = subprocess.check_output(batcmd, shell = True)
	bpm = str(result,'utf-8')
	return bpm

def get_fingerprint(_filename):
    duration, fp_encoded = acoustid.fingerprint_file(_filename)
    fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
    return fingerprint

def main():
	uploader = False
	counter = 0
	if len(sys.argv) == 2 and sys.argv[1] == "upload":
		uploader = True
		print("Entering upload mode")
	pf = os.getcwd()
	for root, dirs, files in os.walk(pf):
		for filename in files:
			if filename != "main.py":
				fingerpre = get_fingerprint(filename)
				fingerpass1 = str(fingerpre).replace("[","")
				finger = str(fingerpass1).replace("]","")
				bpm = get_bpm(filename)
				if uploader == True:
					print(finger)
					print(filename)
					print(bpm)
				#	update_db(filename,str(finger),bpm,"fkk")
				if uploader == False:
					db_connect(finger,bpm)
'''				part1 = []
				part2 = []
#				print(round(len(fingerpre)/2))
				for fingerp in fingerpre:
					if counter < round(len(fingerpre)/2): 
						part1.append(fingerp)
#						part1.append('%')
						counter = counter +1
					else:
						part2.append(fingerp)
#						part2.append('%')

				print("--------------------------------")
				for i in range(1):
					part1fpass1 = str(part1).replace("[","")
					part1fpass2 = str(part1fpass1).replace("]","")
					part1f = str(part1fpass2).replace("\'","")
#					print(part1f)
					db_connect(part1f,bpm)
					part2fpass1 = str(part2).replace("[","")
					part2fpass2 = str(part2fpass1).replace("]","")
					part2f = str(part2fpass2).replace("\'","")
#					print(part2f)
					db_connect(part2f,bpm)
'''
if __name__ == '__main__':
	main()
