# Edit the config here
global WEBHOOK
WEBHOOK = '' # Put a webhook to log uploads
PROXIES = False # Enables proxies on roblox request (won't bypass rate limits, that's based on accounts)
PROXY_FILE = 'proxies.txt' # where to read the proxies from
RANDOMCOOKIE = False # Picks a random cookie for every upload (Can cause problems with big cookie files)
DIRECTORY = 'out' # Where to get the files to upload

if PROXIES:
    try:
        proxy_list = open(PROXY_FILE).readlines()
        proxy_list = [line.strip() for line in proxy_list]
    except:
        print(f'Failed to opend "{PROXY_FILE}" turning off proxy support')
        PROXIES = False # Failed to read file so turn proxy support off

# Rest of the script
from json import dumps
from requests import post
from time import sleep
from random import randint, shuffle, choice
from DecalUploader import DecalClass

if PROXIES: shuffle(proxy_list)

global ROBLOSECURITY
cookies = open("cookies.txt", 'r+').readlines()
cookies = [line.strip() for line in cookies]

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

    status = post(webhook, data=dumps(payload), headers={"Content-Type": "application/json"}).text
    if 'Invalid Webhook Token' in status or 'Unknown Webhook' in status:
        global WEBHOOK
        WEBHOOK = '' # Webhook doesn't exist so don't keep sending stuff

if '__main__' in __name__:
    import os

    clear = input('Clear Out.csv? (Y/N): ')
    if 'y' in clear.lower():
        with open('Out.csv','w') as clr:
            clr.write('FileName,DecalId,ImageId\n') # CSV headers

    cook_num, cookies_num = 0, len(cookies)-1
    a=''
    for filename in os.listdir(DIRECTORY):
        try:
            if PROXIES:
                proxy = choice(proxy_list).strip()
                prox = { 
                    "http"  : proxy,
                    "https" : proxy,
                    }
            else:
                prox = {}

            if RANDOMCOOKIE:
                ROBLOSECURITY = choice(cookies).strip()
            else:
                ROBLOSECURITY = cookies[cook_num].strip()
            f = os.path.join(DIRECTORY, filename) # get the img path
            a = DecalClass(ROBLOSECURITY, f, 'Decal', 'Decal').upload() # Create the upload and upload then get the json data
            while 'BANNED' in a:
                cook_num += 1
                if RANDOMCOOKIE: cookies.remove(ROBLOSECURITY)
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
