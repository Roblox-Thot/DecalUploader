import requests
import json
import os
import urllib.parse
from time import sleep
from random import randint
from bs4 import BeautifulSoup

class DecalClass():
    global classes
    classes = {
        'Audio': 3,
        'Mesh': 4,
        'Lua': 5,
        'Model': 10,
        'Decal': 13,
        'Gear': 19,
        'Plugin': 38,
        'MeshPart': 40
    }

    def __init__(self, cookie:str, location:str, name:str, description:str = 'Studio', type:str = 'Decal', proxy: dict = None):
        '''Set up the DecalClass

        Args:
            cookie (String): The cookie to the account you are uploading to
            location (String): Path to the image
            name (String): Name of the decal
            description (String): Description of the decal
        '''
        if proxy is None: proxy = {}
        
        self.upload_type = classes[type]
        self.request = requests.Session() # Make a request session so its easier later
        self.request.cookies.update({'.ROBLOSECURITY': cookie}) # Setting ROBLOSECURITY cookie
        self.request.headers.update({'User-Agent': 'RobloxStudio/WinInet RobloxApp/0.601.0.6010507 (GlobalDist; RobloxDirectDownload)'})# Sets a the UA to the Roblox Studio
        self.location = location
        self.upload_url = f'https://data.roblox.com/data/upload/json?assetTypeId={self.upload_type}&name={urllib.parse.quote(name)}&description={urllib.parse.quote(description)}'
        self.proxy = proxy

    def getCSRFToken(self):
        '''Gets Roblox's CSRF token for uploading

        Returns:
            string: CSRF token header
        '''
        if token := self.request.post('https://auth.roblox.com/v2/login', proxies=self.proxy).headers[
            'x-csrf-token'
        ]:
            return token
        print('Please log in (X-csrf-token fail)')
        exit() # Lazy hack mate
    
    def upload(self):
        '''Attempts to upload the decal

        Returns:
            JSON: Contains the following>
                'Success' if it was Uploaded correctly

                'AssetId' which is the Decal ID

                'BackingAssetId' which is the Image ID

                'Message' used only if Success is false
        '''
        token = self.getCSRFToken()

        with open(self.location, 'rb') as fp: # Open image as bytes
            data = fp.read() + os.urandom(69)

        headers = {
                    'Requester': 'Client',
                    'X-CSRF-TOKEN': token
                }
        post_data = self.request.post(self.upload_url,headers=headers,data=data, proxies=self.proxy)
        if 'Re-activate My Account' in post_data.text:
            print('Warned attempting to fix')
            try:
                # Get the form data to post
                soup = BeautifulSoup(post_data.content, 'html.parser')
                verification_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
                punishment_id = soup.find('input', {'name': 'punishmentId'})['value']

                # Post the data
                data = {'__RequestVerificationToken':verification_token,'punishmentId':punishment_id}
                header = {'Content-Type':'application/x-www-form-urlencoded'}
                self.request.post('https://www.roblox.com/not-approved/reactivate', data=data, headers=header,proxies=self.proxy)

                post_data = self.upload()
            except Exception:
                input('failed to reactivate')
        elif 'not-approved' in post_data.url:
            print('\n\nbanned')
            return 'BANNED'
        elif 'retry-after' in post_data.headers:
            pause_time = int(post_data.headers['retry-after']) + 1 # Get the retry header and wait 1 extra sec
            print(f'Rate limited for {pause_time} seconds... (Waiting)')
            sleep(pause_time)
            post_data = self.upload() # Retry upload after Rate limit (:skull:)
        return post_data

import contextlib
if '__main__' in __name__:
    import os
    import sys
    try:
        ROBLOSECURITY = open('cookie.txt').readline() # Because this fucker is so lazy ig https://v3rm.net/threads/roblox-decal-tools.144/post-2702
    except Exception:
        ROBLOSECURITY = input('Cookie: ') if len(sys.argv) < 2 else sys.argv[1]
    clear = input('Clear Out.csv? (Y/N): ')
    if 'y' in clear.lower():
        with open('Out.csv','w') as clr:
            clr.write('FileName,DecalId,ImageId\n') # CSV headers

    directory = 'files'
    for filename in os.listdir(directory):
        with contextlib.suppress(Exception):
            f = os.path.join(directory, filename) # get the img path
            a = DecalClass(ROBLOSECURITY, f, os.urandom(2), 'Decal').upload().json() # Create the upload and upload then get the json data
            if 'BANNED' in a:
                print('Cookie was banned.\n')
                ROBLOSECURITY = input('Cookie: ')
                a = DecalClass(ROBLOSECURITY, f, os.urandom(2), 'Decal').upload().json() # Create the upload and upload then get the json data
            if a['Success']:
                with open('Out.csv','a') as out:
                    out.write(f'{filename},{a["AssetId"]},{a["BackingAssetId"]}\n')
                print(f'Uploaded {filename} (AssetID: {a["AssetId"]})')
                os.remove(f)
            else:
                print(filename, a['Message'])
            sleep(randint(0,2)) # Give Roblox a random break
