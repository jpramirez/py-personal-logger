
import json
import sys
import logging
import boto3
import requests
from datetime import datetime
import time 
from os import environ
from sys import exit
from pydub import AudioSegment

mysp=__import__("my-voice-analysis")

TOKEN = environ.get("TELEGRAM_TOKEN", "")

def get_audio(audio,chat_id):
    print("GET_AUDIO")
    FILE_URL = "https://api.telegram.org/bot{}/getFile?file_id={}".format(TOKEN,audio.file_id)
    request_file_info = requests.get(FILE_URL)
    print (request_file_info)
    file_info = request_file_info.json()
    ret = get_file(file_info,chat_id)
    return ret

def get_file (file_info,chat_id):
    client = boto3.client('s3')
    print("GET_FILE")

    FILE_URL2 ="https://api.telegram.org/file/bot{}/{}".format(TOKEN,file_info['result']['file_path'])
    print(FILE_URL2)
    file_path = download_file(FILE_URL2)
    s3_path = "{}/{}/{}".format(chat_id, datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),file_info['result']['file_path']) 
    client.upload_file(file_path, "py-audio-logger" , s3_path)
    return True


def convert_ogg_to_wav(original,destination):
    song = AudioSegment.from_ogg(original)
    song.export(destination, format="wav")

def detect_gender(folder, file):
    mysp.mysppaus(folder,file)

def download_file(url):
    folder = "Audio/"
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(folder + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    convert_ogg_to_wav(folder + local_filename, folder + local_filename + ".wav" )
    detect_gender (folder, local_filename)
    return folder + local_filename

