import requests
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

    def __init__(self, cookie:str, location:str, name:str, description:str = 'Studio', type:str = 'Decal'):
        """Set up the DecalClass

        Args:
            cookie (String): The cookie to the account you are uploading to
            location (String): Path to the image
            name (String): Name of the decal
            description (String): Description of the decal
        """
        self.uploadType = classes[type]
        self.request = requests.Session() # Make a request session so its easier later
        self.request.cookies.update({'.ROBLOSECURITY': cookie}) # Setting ROBLOSECURITY cookie
        self.request.headers.update({'User-Agent': 'RobloxStudio/WinInet RobloxApp/0.609.0.6090385 (GlobalDist; RobloxDirectDownload)'})# Sets a the UA to the Roblox Studio
        self.location = location
        self.uploadURL = f'https://data.roblox.com/data/upload/json?assetTypeId={self.uploadType}&name={urllib.parse.quote(name)}&description={urllib.parse.quote(description)}'

    def getCSRFToken(self):
        """Gets Roblox's CSRF token for uploading

        Returns:
            string: CSRF token header
        """
        if token := self.request.post('https://auth.roblox.com/v2/login').headers[
            'x-csrf-token'
        ]:
            return token
        print('Please log in (X-csrf-token fail)')
        exit() # Lazy hack mate
    
    def upload(self):
        """Attempts to upload the decal

        Returns:
            JSON: Contains the following>
                'Success' if it was Uploaded correctly

                'AssetId' which is the Decal ID

                'BackingAssetId' which is the Image ID

                'Message' used only if Success is false
        """
        token = self.getCSRFToken()
        
        with open(self.location, 'rb') as dick: # Open image as bytes
            data = dick.read() + os.urandom(69)

        headers = {
                    'Requester': 'Client',
                    'X-CSRF-TOKEN': token
                }
        PData = self.request.post(self.uploadURL,headers=headers,data=data)
        if 'Re-activate My Account' in PData.text:
            print('Warned attempting to fix')
            try:
                # Get the form data to post
                soup = BeautifulSoup(PData.content, 'html.parser')
                verification_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
                punishmentId = soup.find('input', {'name': 'punishmentId'})['value']

                # Post the data
                self.request.post('https://www.roblox.com/not-approved/reactivate', data={'__RequestVerificationToken':verification_token,'punishmentId':punishmentId}, headers={'Content-Type':'application/x-www-form-urlencoded'})

                PData = self.upload()
            except:
                input('failed to reactivate')
        elif 'not-approved' in PData.url:
            input('banned/warned pls check (press enter to retry upload)') # Pause... are you banned/warned... thats cringe
            PData = self.upload() # Retry upload after the user hits enter
        elif 'retry-after' in PData.headers:
            pausetime = int(PData.headers['retry-after']) + 1 # Get the retry header and wait 1 extra sec
            print(f'Rate limited for {pausetime} seconds... (Waiting)')
            sleep(pausetime)
            PData = self.upload() # Retry upload after Rate limit (:skull:)
        return PData

if '__main__' in __name__:
    import os
    import sys
    try:
        ROBLOSECURITY = open('cookie.txt').readline() # Because this fucker is so lazy ig https://v3rm.net/threads/roblox-decal-tools.144/post-2702
    except:
        if len(sys.argv) < 2:
            ROBLOSECURITY = input('Cookie: ')
        else:
            ROBLOSECURITY = sys.argv[1]

    clear = input('Clear Out.csv? (Y/N): ')
    if 'y' in clear.lower():
        with open('Out.csv','w') as clr:
            clr.write('FileName,DecalId,ImageId\n') # CSV headers

    directory = 'files'
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename) # get the img path
            a = DecalClass(ROBLOSECURITY, f, os.urandom(2), 'Uploaded with studio').upload().json() # Create the upload and upload then get the json data
            if a['Success']:
                with open('Out.csv','a') as out:
                    out.write(f'{filename},{a["AssetId"]},{a["BackingAssetId"]}\n')
                print(f'Uploaded {filename} (AssetID: {a["AssetId"]})')
                os.remove(f)
            else:
                print(filename, a['Message'])
            sleep(randint(0,2)) # Give Roblox a random break
        except:
            pass # something somewhere is broken idc to debug rn
