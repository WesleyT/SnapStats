import os
import sys
import json
import io
import clr

#Script Info
ScriptName = "Snap Stats"
Website = "https://www.weazol.com"
Description = "A Script to assist with displaying snap stats in OBS"
Creator = "Weazol"
Version = "1.0"

settingsFile = "settings.json"
settings = {}
topdir = os.path.dirname(__file__)

# Initialize  
def Init():
    global settings
    
    try:
        with io.open(os.path.join(topdir, settingsFile), encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8-sig")
    except:
        settings = {
            "CurrentRank": 10,
            "RankCubes": 0,
            "HighestRank": 10,
            "CollectionLevel": 50,
            "Permission": "Moderator",
            "Username": ""
            }

    #   Create Stats Directory
    directory = os.path.join(topdir, "Stats")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Create Stats Files
    path = os.path.join(topdir, "Stats\current_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(settings["CurrentRank"]))

    path = os.path.join(topdir, "Stats\highest_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(settings["HighestRank"]))

    path = os.path.join(topdir, "Stats\collection_level.txt")
    with io.open(path, "w") as f:
        f.write(str(settings["CollectionLevel"]))

    path = os.path.join(topdir, "Stats\current_rank_cubes.txt")
    with io.open(path, "w") as f:
        f.write(str(settings["RankCubes"]))

    path = os.path.join(topdir, "Stats\cubes_today.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")

    path = os.path.join(topdir, "Stats\wins.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")

    path = os.path.join(topdir, "Stats\losses.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")

    return

# Execute Data
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == "!thistest" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        Parent.SendStreamMessage("has worked")    # Send your message to chat
    return

# Tick method 
def Tick():
    return

#unused Parse method
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString


# Reload/Save Settings
def ReloadSettings(jsonData):
    Init()
    
    Parent.Log(ScriptName, str(settings["CurrentRank"]))

        
    return

# Unload
def Unload():
    return

# Script Toggle
def ScriptToggled(state):
    return
