WEBHOOK = '' # Put a webhook to log uploads

import requests
import json
from time import sleep
from random import randint
from DecalUploader import DecalClass

global ROBLOSECURITY
cookies = open("cookies.txt", 'r+').readlines()

def send_discord_message(webhook,name_value,decal_value,img_value):
    decal_value = int(decal_value)
    img_value = int(img_value)
    library_url = f"https://www.roblox.com/library/{img_value}/"

    embed_data = {
        "title": "Uploaded",
        "url": library_url,
        "fields": [
            {"name": "File Name", "value": f"{name_value}"},
            {"name": "Decal Id", "value": f"{decal_value}"},
            {"name": "Image ID", "value": f"{img_value}"}
        ],
        "color": "16777215"
    }

    payload = {"embeds": [embed_data]}

    requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json"})

if '__main__' in __name__:
    import os

    clear = input('Clear Out.csv? (Y/N): ')
    if 'y' in clear.lower():
        with open('Out.csv','w') as clr:
            clr.write('FileName,DecalId,ImageId\n') # CSV headers

    directory = 'out'
    cook_num, cookies_num = 0, len(cookies)-1
    a=''
    for filename in os.listdir(directory):
        try:
            ROBLOSECURITY = cookies[cook_num].strip()
            f = os.path.join(directory, filename) # get the img path
            a = DecalClass(ROBLOSECURITY, f, 'Decal', 'Decal').upload() # Create the upload and upload then get the json data
            while 'BANNED' in a:
                cook_num += 1
                if cook_num > cookies_num:
                    print("Out of cookies\nExiting...")
                    exit()
                else:
                    print('Cookie was banned, going to next cookie...')
                    ROBLOSECURITY = cookies[cook_num].strip()
                    a = DecalClass(ROBLOSECURITY, f, 'Decal', 'Decal').upload() # Retry upload
            
            if type(a) != dict: a=a.json() # Set the data to Json if it's not already

            if a['Success']:
                with open('Out.csv','a') as out:
                    out.write(f'{filename},{a["AssetId"]},{a["BackingAssetId"]}\n')
                print(f'Uploaded {filename} (AssetID: {a["AssetId"]})')
                if WEBHOOK != '':
                    send_discord_message(WEBHOOK,filename,a['AssetId'],a['BackingAssetId'])
                os.remove(f)
            else:
                print(filename, a['Message'])
            sleep(randint(0,2)) # Give Roblox a random break
        except Exception as e:
            print(e)
            pass # something somewhere is broken idc to debug rn
