import requests
import urllib.parse

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
        self.name = name
        self.uploadURL = f'https://data.roblox.com/data/upload/json?assetTypeId=13&name={urllib.parse.quote(name)}&description=a'

    def getCSRFToken(self): # Roblox's cringe token system
        token = self.request.post("https://auth.roblox.com/v2/login").headers['x-csrf-token']
        if token:
            return token
        else:
            print("Please log in (X-csrf-token fail)"); exit() # Lazy hack mate
    
    def upload(self):
        token = self.getCSRFToken()
        
        with open(self.location, 'rb') as dick: # Open image as bytes
            data = dick.read()
        files = {'file': ('image.png', data, 'image/png')} # Add image as files data

        headers = {"Requester": "Client",
                    "X-CSRF-TOKEN": token
                }
        return self.request.post(self.uploadURL,headers=headers,data=data).json()



if "__main__" in __name__:
    import os
    ROBLOSECURITY = input("Cookie: ")
    a = DecalClass(ROBLOSECURITY, "IMG_6887.jpeg", "test").upload()
    print(a)