#
# Hello there! Welcome to Mod Mode Scripts!
# Mod Scripts are Python scripts that you can make to run code like configuring your bootstrap/Roblox functionality 
# and sending a notification for when Roblox crashes!
# If you're a python developer, you may be able to get started here!
# If you're a person who would like to run multiple mods, you'll only be able to run 1 script at a time due to security, so choose wisely!
# 

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
def onRobloxAppStart(data):
    template_count = EfazRobloxBootstrapAPI.getConfiguration("template_count") or 0
    template_count += 1
    EfazRobloxBootstrapAPI.setConfiguration("template_count", template_count)
    printWarnMessage("--- Template ---")
    printMainMessage("Hello there!")
    printMainMessage("This is a template mod script here!")
    printMainMessage("This is ran when Roblox opened earlier.")
    printMainMessage("If you know python, try editing this script from the Template Mod folder and installing through Install.py!")
    printDebugMessage(f"You can only see this if you're in debug mode! Template Mod Script has ran {template_count} times!")
    printWarnMessage("--- Template ---")
def onRobloxCrash(data):
    printMainMessage("Oof! Roblox crashed!")
def onBloxstrapSDK(data):
    printMainMessage("Bloxstrap SDK requested!")
def onRobloxPassedUpdate(data):
    printSuccessMessage("Woo hoo! Roblox passed the update check!")
def onGameDisconnected(data):
    printErrorMessage("The template script detected the game disconnect. :(")
def onGameJoined(data):
    printSuccessMessage("Woo hoo! The template script detected you joined a game!")