import requests
import urllib.parse
from time import sleep
from random import randint

classes = {
    "Image": 1,
    "TShirt": 2,
    "Audio": 3,
    "Mesh": 4,
    "Lua": 5,
    "Hat": 8,
    "Place": 9,
    "Model": 10,
    "Shirt": 11,
    "Pants": 12,
    "Decal": 13,
    "Head": 17,
    "Face": 18,
    "Gear": 19,
    "Badge": 21,
    "Animation": 24,
    "Torso": 27,
    "RightArm": 28,
    "LeftArm": 29,
    "LeftLeg": 30,
    "RightLeg": 31,
    "Package": 32,
    "GamePass": 34,
    "Plugin": 38,
    "MeshPart": 40,
    "Video": 62,
    "FontFamily": 73,
    "MoodAnimation": 78,
    "DynamicHead": 79
}

class DecalClass():
    def __init__(self, cookie:str, location:str, name:str, description:str = "Studio", type:str = "Decal"):
        """Set up the DecalClass

        Args:
            cookie (String): The cookie to the account you are uploading to
            location (String): Path to the image
            name (String): Name of the decal
            description (String): Description of the decal
        """
        self.uploadType = classes[type.lower()]
        self.request = requests.Session() # Make a request session so its easier later
        self.request.cookies.update({'.ROBLOSECURITY': cookie}) # Setting ROBLOSECURITY cookie
        self.request.headers.update({"User-Agent": "RobloxStudio/WinInet RobloxApp/0.601.0.6010507 (GlobalDist; RobloxDirectDownload)"})# Sets a the UA to the Roblox Studio
        self.location = location
        self.uploadURL = f'https://data.roblox.com/data/upload/json?assetTypeId={self.uploadType}&name={urllib.parse.quote(name)}&description={urllib.parse.quote(description)}'

    def getCSRFToken(self):
        """Gets Roblox's CSRF token for uploading

        Returns:
            string: CSRF token header
        """
        if token := self.request.post("https://auth.roblox.com/v2/login").headers[
            'x-csrf-token'
        ]:
            return token
        print("Please log in (X-csrf-token fail)")
        exit() # Lazy hack mate
    
    def upload(self):
        """Attempts to upload the Asset

        Returns: (Only documented for decals)
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
            input("banned/warned pls check (press enter to retry upload)") # Pause... are you banned/warned... thats cringe
            PData = self.upload() # Retry upload after the user hits enter
        elif 'retry-after' in PData.headers:
            pausetime = int(PData.headers["retry-after"]) + 1 # Get the retry header and wait 1 extra sec
            print(f'Rate limited for {pausetime} seconds... (Waiting)')
            sleep(pausetime)
            PData = self.upload() # Retry upload after Rate limit (:skull:)
        return PData

if "__main__" in __name__:
    import os
    ROBLOSECURITY = input("Cookie: ")

    clear = input("Clear Out.csv? (Y/N): ")
    if "y" in clear.lower():
        with open("Out.csv",'w') as clr:
            clr.write("FileName,DecalId,ImageId\n") # CSV headers

    directory = 'files'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename) # get the img path
        a = DecalClass(ROBLOSECURITY, f, filename).upload().json() # Create the upload and upload then get the json data
        if a["Success"]:
            with open("Out.csv",'a') as out:
                out.write(f'{filename},{a["AssetId"]},{a["BackingAssetId"]}\n')
            print(f'Uploaded {filename} (AssetID: {a["AssetId"]})')
            os.remove(f)
        else:
            print(filename, a["Message"])
        sleep(randint(0,2)) # Give Roblox a random break
