import requests
import os
from bs4 import BeautifulSoup
from time import sleep
import urllib3

urllib3.disable_warnings()

class DecalClass():
    def __init__(self, cookie, location, name):
        self.goose = requests.Session()
        self.goose.cookies.update({
            '.ROBLOSECURITY': cookie #set .ROBLOSECURITY cookie for authentication
        })
        self.goose.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134", #might as well use a User Agent
        })
        self.location = location
        self.name = name
    def getToken(self): #get verification token function
        homeurl= 'https://www.roblox.com/build/upload' #this is the upload endpoint
        response = self.goose.get(homeurl, verify=False)
        try:
            soup = BeautifulSoup(response.text, "lxml")
            veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"] #parse out the verification token from the HTML
        except NameError:
            print(NameError)
            return False
        return veri
    def upload(self):
        with open(self.location, 'rb') as dick:
            random_bytes = os.urandom(10)
            data = dick.read() + random_bytes
        files = {'file': ('image.png', data, 'image/png')} #add our image as files data
        data = {
            '__RequestVerificationToken': self.getToken(),
            'assetTypeId': '13', #we use assetTypeId '13' because 13 is the id for Decals
            'isOggUploadEnabled': 'True',
            'isTgaUploadEnabled': 'True',
            
            'onVerificationPage': "False",
            "captchaEnabled": "True",
            'name': self.name
        }
        try:
            response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data) #make the request
            if "You are uploading too much" in response.text:
                print("rate limited waiting 40 sec")
                sleep(40)
                response = self.upload()
            elif "Banned" in response.text or "not-approved" in response.url:
                input("banned/warned pls check (press enter to continue)")
                response = self.upload()
            return response
        except:
            print("error is making request")


ROBLOSECURITY = input("Cookie: ")

if "Y" input("Clear Out.txt? (Y/N): "):
    with open("Out.txt",'w') as out:
        pass # Lazy clear lmao

directory = 'files'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    a = DecalClass(ROBLOSECURITY, f, filename).upload()
    url = str(a.url)
    if "&uploadedId=" in url:
        with open("Out.txt",'a') as out:
            url = url.replace("https://www.roblox.com/build/upload?assetTypeId=13&uploadedId=","https://roblox.com/library/")
            out.write(f'{url}\n')
            print(a.status_code, url)
    else:
        print(a.status_code, url)
