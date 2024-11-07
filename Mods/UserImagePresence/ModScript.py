#
# UserImagePresence is a mod made by Efaz that would replace the Efaz's Roblox Bootstrap logo in the Discord Presence with your user profile image and name!
# It is an idea that is referenced from Bloxstrap
# 

# Python Modules
import requests
import time

# Load Bootstrap API
import EfazRobloxBootstrapAPI as ERBAPI; EfazRobloxBootstrapAPI = ERBAPI.EfazRobloxBootstrapAPI()
debugMode = EfazRobloxBootstrapAPI.getDebugMode()
apiVersion = EfazRobloxBootstrapAPI.about()
    
# Printing Functions
def printMainMessage(mes): # White System Console Text
    if apiVersion and type(apiVersion.get("api_version")) is dict and apiVersion.get("api_version").get("version", "1.0.0") < "1.3.6":
        print(f"\033[38;5;255m[MOD SCRIPT]: {mes}\033[0m")
    else:
        EfazRobloxBootstrapAPI.printMainMessage(mes)
def printErrorMessage(mes): # Error Colored Console Text
    if apiVersion and type(apiVersion.get("api_version")) is dict and apiVersion.get("api_version").get("version", "1.0.0") < "1.3.6":
        print(f"\033[38;5;196m[MOD SCRIPT]: {mes}\033[0m")
    else:
        EfazRobloxBootstrapAPI.printErrorMessage(mes)
def printSuccessMessage(mes): # Success Colored Console Text
    if apiVersion and type(apiVersion.get("api_version")) is dict and apiVersion.get("api_version").get("version", "1.0.0") < "1.3.6":
        print(f"\033[38;5;82m[MOD SCRIPT]: {mes}\033[0m")
    else:
        EfazRobloxBootstrapAPI.printSuccessMessage(mes)
def printWarnMessage(mes): # Orange Colored Console Text
    print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): # Yellow Colored Console Text
    if apiVersion and type(apiVersion.get("api_version")) is dict and apiVersion.get("api_version").get("version", "1.0.0") < "1.3.6":
        print(f"\033[38;5;226m[MOD SCRIPT]: {mes}\033[0m")
    else:
        EfazRobloxBootstrapAPI.printWarnMessage(mes)
def printDebugMessage(mes): # Debug Console Text
    if apiVersion and type(apiVersion.get("api_version")) is dict and apiVersion.get("api_version").get("version", "1.0.0") < "1.3.6":
        if debugMode == True: print(f"\033[38;5;226m[MOD SCRIPT]: {mes}\033[0m")
    else:
        EfazRobloxBootstrapAPI.printDebugMessage(mes)

# Main Handler
userInfo = None
disconnected = True
def onGameJoinInfo(data):
    global userInfo
    global disconnected

    disconnected = False
    if data and data.get("username") and data.get("userId"):
        thumbnail_res = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={data.get('userId')}&size=100x100&format=Png&isCircular=false")
        if thumbnail_res.ok:
            thumbnail_json = thumbnail_res.json()
            if thumbnail_json and len(thumbnail_json.get("data", [])) > 0:
                user_thumbnail = thumbnail_json["data"][0].get("imageUrl")
                if user_thumbnail:
                    data["thumbnail"] = user_thumbnail
                    userInfo = data
                    printSuccessMessage(f"Loaded user @{data.get('username')} [User ID: {data.get('userId')}]!")
                    printDebugMessage(f"Loaded thumbnail: {user_thumbnail}")
                else:
                    userInfo = None
                    printErrorMessage(f"Failed to load thumbnail for @{data.get('username')} [User ID: {data.get('userId')}]! Status Code: {thumbnail_res.status_code}")
            else:
                userInfo = None
                printErrorMessage(f"Failed to load thumbnail for @{data.get('username')} [User ID: {data.get('userId')}]! Status Code: {thumbnail_res.status_code}")
        else:
            userInfo = None
            printErrorMessage(f"Failed to load thumbnail for @{data.get('username')} [User ID: {data.get('userId')}]! Status Code: {thumbnail_res.status_code}")
        if userInfo:
            while (disconnected == False):
                time.sleep(0.1)
                EfazRobloxBootstrapAPI.sendBloxstrapRPC("SetRichPresence", {
                    "smallImage": {
                        "assetId": userInfo.get("thumbnail"),
                        "hoverText": f"Playing @{userInfo.get('username')} as {userInfo.get('displayName')}!"
                    }
                }, True)
def onGameDisconnected(data):
    global disconnected
    disconnected = True