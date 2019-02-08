#!/usr/bin/python3
import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType
import pyaudio
import wave
#TTS
import pyttsx3
#For local CMD exe
import subprocess
#Speech recognition
import speech_recognition as sr
#DB Connector
import mysql.connector
from time import sleep

def TTS(phase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(phase)
    engine.runAndWait()

def start():
    while 1:
        rec()
        sleep(0.5)

def rec():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
    #stream = p.open(format = FORMAT,rate = RATE,channels = CHANNELS, input_device_index = 2,input = True, frames_per_buffer = CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    sleep(1)
    recg(WAVE_OUTPUT_FILENAME)

def recg(filename):
    config = {
        'host':'identify-eu-west-1.acrcloud.com',
        'access_key':'c9098ed9fe58c7dfc3a33356a0cd70fd',
        'access_secret':'yJy4G4wOn6WG5Mdli8NW9KvRoroMoKoIS0VEtdSh',
        'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_AUDIO, # you can replace it with [ACR_OPT_REC_AUDIO,ACR_OPT_REC_HUMMING,ACR_OPT_REC_BOTH], The     SDK decide which type fingerprint to create accordings to "recognize_type".
        'debug':False,
        'timeout':10 # seconds
    }
    
    re = ACRCloudRecognizer(config)

    print("duration_ms = " + str(ACRCloudRecognizer.get_duration_ms_by_file(filename)))
    print("sec = " + str(ACRCloudRecognizer.get_duration_ms_by_file(filename) * 0.001))
    print("min = "+str(ACRCloudRecognizer.get_duration_ms_by_file(filename) /60000))

    buf = open(filename, 'rb').read()
    result = re.recognize_by_filebuffer(buf, 0, 10)
    print(result)
    if result == "{\"status\":{\"msg\":\"No result\",\"code\":1001,\"version\":\"1.0\"}}\n":
        TTS("Song Not found")
    else:
        start = 0
        end = 0
        title = result.find("title")
        label = result.find("label")
        resl = result.find("release_date")
        art = result.find("artists")
        
        if resl > label:
            end = resl
        else: 
            end = label
        if title < art:
            start = title
        else:
            start = art
        
        pass1 = result[start:end]
        pass1_num_start = pass1.find("title\":")
        pass1_num_end = pass1.find("\",\"")
        pass1_num_art_start= pass1.find("artists")
        pass1_num_art_end = pass1.find("],\"")
        
        if pass1_num_end > pass1_num_start:
            titlef = pass1[pass1_num_start:pass1_num_end]
            artf = pass1[pass1_num_art_start:pass1_num_art_end]
        else:
            titlef = pass1[pass1_num_start:pass1_num_end]
            artf = pass1[0:pass1_num_start]
        if len(titlef) != 0:
            print(titlef.replace("\"","").replace(",",""))
            print(artf.replace("\"","").replace("{name:","").replace("[","").replace("}","").replace("]",""))
            TTS("The song is " +titlef.replace("\"","").replace(",","").replace("title:","") + " by "+ artf.replace("\"","").replace("{name:","").replace("[","").replace("}","").replace("]","").replace("artists:",""))
        else:
            TTS("Song Not found")

if __name__ == '__main__':
    start()
   
