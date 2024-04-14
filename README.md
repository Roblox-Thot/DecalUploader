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

<div align="center"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Roblox-Thot/DecalUploader">DecalUploader</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Roblox-Thot">Olivia Moore</a> is licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p></div>
