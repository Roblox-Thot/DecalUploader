import requests
import urllib.parse

class DecalClas():
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
        self.endpoint = "https://data.roblox.com/data/upload/json?assetTypeId=13&name=Images%2Fbarak&description=madeinstudio"

    def getCSRFToken(self): # Roblox's cringe token system
        return requests.post("https://auth.roblox.com/v2/logout").headers["x-csrf-token"]
    