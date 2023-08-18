# Start the Python Script
import requests # Used to send the requests
from bs4 import BeautifulSoup # Used to grab the token in getToken
from time import sleep # Import a eepy function for ratelimits
# Empty line to make it cleaner
try: # Attempts to hide urllib3 warnings
    from urllib3 import disable_warnings # Import disable function
    disable_warnings() # Run the imported function
except: # If for what ever reason it fails just ignore it lol
    pass # Ignor
# Empty line to make it cleaner
class DecalClass():  # Create class
    def __init__(self, cookie:str, location:str, name:str): # Init function that fires when you make a DecalClass
        """Set up the DecalClass

        Args:
            cookie (String): The cookie to the account you are uploading to
            location (String): Path to the image
            name (String): Name of the decal
        """ # Doc String
        self.goose = requests.Session() # Make a request session for an upload
        self.goose.cookies.update({'.ROBLOSECURITY': cookie}) # Setting ROBLOSECURITY so you CAN upload
        self.goose.headers.update({"User-Agent": "RobloxGameCloud/1.0 (+http://www.roblox.com)"})# Sets a User Agent because yes
        self.location = location # Set the file location
        self.name = name # Set the name of the upload
        self.endpoint = "https://www.roblox.com/build/upload" # Upload endpoint
# Empty line to make it cleaner
    def getToken(self): # Make a function to get a token
        """Get verification token function

        Can return:
            String: RequestVerificationToken Token
            False: Failed to get the token (NameError)
        """ # Doc String
        response = self.goose.get(self.endpoint, verify=False) # Send a request to get a token
        if "not-approved" in response.url: # Check for a moderated redirect
            input("banned/warned pls check (press enter to continue)") # Pause... are you banned/warned... thats cringe
            return self.upload() # Retry upload after the user hits enter
        try: # Attempt to grab a token
            soup = BeautifulSoup(response.text, "lxml")
            veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"] #parse out the verification token from the HTML
        except NameError: # Catch any ne errors
            print(NameError) # Print error
            return False # Return false since it failed :kek:
        return veri # Return token
# Empty line to make it cleaner
    def upload(self): # Create upload function
        """Upload the set items

        Returns:
            Response data: The normal data you would get from a request
        """# Doc String
        with open(self.location, 'rb') as dick: # Open image as bytes
            random_bytes = os.urandom(10) # Make random bytes
            data = dick.read() + random_bytes # Add random bytes to the image (idfk)
        files = {'file': ('image.png', data, 'image/png')} # Add image as files data
        data = { # Set data for the upload
            '__RequestVerificationToken': self.getToken(), # Get a token to upload (Roblox is cringe)
            'assetTypeId': '13', # 13 is the id used for Decals
# Empty line to make it cleaner
            'onVerificationPage': "False", # IDK if its neede
            "captchaEnabled": "True", # IDK if its neede
            'name': self.name # Name of file
        }# Close data json
        try: # Lets try this upload attempt
            response = self.goose.post(self.endpoint, files=files, data=data) # Make the request
            if "You are uploading too much" in response.text: # Check for a ratelimit message
                print("rate limited waiting 40 sec") # Let user know its rate limited for now
                sleep(40) # Wait 40 sec, and idfk if this is the best timeout but it works 90% of the time
                response = self.upload() # Retry upload
            elif "not-approved" in response.url: # Check for a moderated redirect
                input("banned/warned pls check (press enter to continue)") # Pause... are you banned/warned... thats cringe
                response = self.upload() # Retry upload after the user hits enter
            return response # Return the request's response
        except: # Catch the error
            print("error is making request") #error
# Empty line to make it cleaner
if "__main__" in __name__: # Run folder upload if the file is ran
    import os # Used for the folder upload
    ROBLOSECURITY = input("Cookie: ") # As user for the cookie
# Empty line to make it cleaner
    clear = input("Clear Out.txt? (Y/N): ")
    if "y" in clear.lower(): # I could do equal check but this is funnier
        with open("Out.txt",'w') as clr:
            pass # Lazy clear lmao
# Empty line to make it cleaner
    directory = 'files' # The name of the folder to look in
    checkFor = "&uploadedId=" # The part in the URL that has the ID in it
    for filename in os.listdir(directory): # Loop in the folder ov
        f = os.path.join(directory, filename) # Get the path to the file in the folder
        a = DecalClass(ROBLOSECURITY, f, filename).upload() # Set up the DecalClass to upload then upload (lazy)
        url = str(a.url) # Over kill setting it to string but idfk I did it anyway
        if checkFor in url: # Roblox passes the ID in a redirect so getting it there is quicker
            with open("Out.txt",'a') as out: # Save the ID as a Library link to make opening it quicker
                uploadedId = url[url.find(checkFor) + len(checkFor):] # Get the ID from the URL in a lazy way
                url = f'https://roblox.com/library/{uploadedId}' # Convert url
                out.write(f'{url}\n') # Write the URL
                print(a.status_code, url) # Prints are just so you know its working lol
        else: # The url didn't have the ID or did but no &
            print(a.status_code, url) # If you see this than it prob failed to upload
# End the script and a new line so GH likes me
