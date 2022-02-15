import json
import sys
import logging
import boto3
import requests
from datetime import datetime
import time 


TELE_TOKEN='5233481227:AAHrH1wpDDwGQT7rSTUvICdR6FCH3aJZV5w'
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

def send_message(text, chat_id):
    final_text = text
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    print (url)
    ret = requests.get(url)
    print (ret)



def get_audio(audio,chat_id):
    print("GET_AUDIO SLEEPING 3")
    time.sleep(3)
    FILE_URL = "https://api.telegram.org/bot{}/getFile?file_id={}".format(TELE_TOKEN,audio['file_id'])
    request_file_info = requests.get(FILE_URL)
    print ("request_file_info" + request_file_info)
    file_info = request_file_info.json()
    ret = get_file(file_info,chat_id)
    print (ret)

def get_file (file_info,chat_id):
    client = boto3.client('s3')
    print("GET_FILE Sleeping 3")
    time.sleep(3)
    FILE_URL2 ="https://api.telegram.org/file/bot{}/{}".format(TELE_TOKEN,file_info['result']['file_path'])
    print(FILE_URL2)
    file_content = requests.get(FILE_URL2)
    file_path =  "/tmp/{}.oga".format(file_info['result']['file_id'])
    data_file = open(file_path, 'w+')
    data_file.write(str(file_content))
    data_file.close()
    s3_path = "{}/{}/{}".format(chat_id, datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),file_info['result']['file_path']) 
    client.upload_file(file_path, "py-audio-logger" , file_info['result']['file_id'])
    
    
def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    reply = "Message received"
    print (reply)
    if 'text' in message['message']:
        reply = "Text Found"
    print (reply)

    if 'voice' in message['message']:
        reply = "Processing Audio"
        ret = get_audio (message['message']['voice'],chat_id)
        if ret == True:
            reply = "Audio Processed"
            
            
    print(reply)

    send_message(reply, chat_id)
    
    return {
        'statusCode': 200
    }






