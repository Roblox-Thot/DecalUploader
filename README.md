# DecalUploader
Simple mass Roblox decal uploader

> [!NOTE]\
> You need to intall `requests` module if you don't have it already

# How to use
There are 2 ways you can use this
## 1. Auto folder uploading
1. Put `DecalUploader.py` in a folder
2. Make a `files` folder next to `DecalUploader.py`
3. Run `DecalUploader.py` and wait for it to stop
4. All decal links will be in `Out.csv` next to `DecalUploader.py`
## 2. As a module
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
