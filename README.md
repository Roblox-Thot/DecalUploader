From now on this will only get fixes, if the API goes down, too bad just use [Roblox-Thot/DecalUploaderV2](https://github.com/Roblox-Thot/DecalUploaderV2)

# DecalUploader
Simple mass Roblox decal uploader

If you use it for a project you can credit me or not I don't really care tbh

If you want an ID checker that works with the output check [MilkKoun/Roblox-Ids-Checker](https://github.com/MilkKoun/Roblox-Ids-Checker)

> [!NOTE]\
> You need to intall `requests` module if you don't have it already

# How to use
There are 2 ways you can use this
## 1. Auto folder uploading
1. Put `DecalUploader.py` in a folder
2. Make a `files` folder next to `DecalUploader.py`
3. Run `DecalUploader.py` and wait for it to stop
4. All decal links will be in `Out.csv` next to `DecalUploader.py`
## 2. Mass cookie upload
1. Download both `.py` files and put them in the same folder
2. Open `MassCookieUpload.py` and edit config
3. Put cookies into a txt file called "cookies"
4. Then just run MassCookieUpload.py
## 3. As a module
```python
from DecalUploader import DecalClass

reply = DecalClass("cookie","fileLocation","uploadName","uploadDescription").upload()
```
the return of Upload will be one of the following JSON datasets

### Successful upload:
```json
{
    "Success": true, If the upload worked
    "AssetId": 1, Decal ID
    "BackingAssetId": 2 Image ID
}
```

### Failed to upload:
```json
{
    "Success": false, If the upload worked
    "Message": "The name or description contains inappropriate text" The reason why it failed
}
```

![image](https://github.com/Roblox-Thot/DecalUploader/assets/67937010/06943b8d-fd15-4cea-9311-a824fe3ca897)
