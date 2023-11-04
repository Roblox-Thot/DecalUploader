import requests
import urllib.parse
from time import sleep

class DecalClass():
    def __init__(self, cookie:str, location:str, name:str):
        """Set up the DecalClass

        Args:
            cookie (String): The cookie to the account you are uploading to
            location (String): Path to the image
            name (String): Name of the decal
        """
        self.request = requests.Session() # Make a request session so its easier later
        self.request.cookies.update({'.ROBLOSECURITY': cookie}) # Setting ROBLOSECURITY cookie
        self.request.headers.update({"User-Agent": "RobloxStudio/WinInet RobloxApp/0.601.0.6010507 (GlobalDist; RobloxDirectDownload)"})# Sets a the UA to the Roblox Studio
        self.location = location
        self.uploadURL = f'https://data.roblox.com/data/upload/json?assetTypeId=13&name={urllib.parse.quote(name)}&description=a'

    def getCSRFToken(self):
        """Gets Roblox's CSRF token for uploading

        Returns:
            string: CSRF token header
        """
        token = self.request.post("https://auth.roblox.com/v2/login").headers['x-csrf-token']
        if token:
            return token
        else:
            print("Please log in (X-csrf-token fail)"); exit() # Lazy hack mate
    
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
            data = dick.read()

        headers = {"Requester": "Client",
                    "X-CSRF-TOKEN": token
                }
        PData = self.request.post(self.uploadURL,headers=headers,data=data)
        if "not-approved" in PData.url:
            input("banned/warned pls check (press enter to continue)") # Pause... are you banned/warned... thats cringe
            PData = self.upload() # Retry upload after the user hits enter
        elif 'retry-after' in PData.headers:
            pausetime = int(PData.headers["retry-after"])+3
            print(f'Rate limited for {pausetime} seconds... (Waiting)')
            sleep(pausetime)
        return PData

if "__main__" in __name__:
    import os
    ROBLOSECURITY = input("Cookie: ")

    clear = input("Clear Out.csv? (Y/N): ")
    if "y" in clear.lower():
        with open("Out.csv",'w') as clr:
            clr.write("FileName,DecalId,ImageId")

    directory = 'files'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        a = DecalClass(ROBLOSECURITY, f, filename).upload()
        print(a)
        a = a.json()
        if a["Success"]:
            with open("Out.csv",'a') as out:
                out.write(f'{filename},{a["AssetId"]},{a["BackingAssetId"]}\n')
            print(f'Uploaded {filename} (AssetID: {a["AssetId"]})')
            os.remove(f)
        else:
            print(filename, a["Message"])
