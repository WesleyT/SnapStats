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

    global CurrentRank
    CurrentRank = settings["CurrentRank"] 
    global HighestRank
    HighestRank = settings["HighestRank"]
    global CollectionLevel
    CollectionLevel = settings["CollectionLevel"]
    global RankCubes
    RankCubes = settings["RankCubes"]

    #   Create Stats Directory
    directory = os.path.join(topdir, "Stats")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Create Stats Files
    path = os.path.join(topdir, "Stats\current_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(CurrentRank))

    path = os.path.join(topdir, "Stats\highest_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(HighestRank))

    path = os.path.join(topdir, "Stats\collection_level.txt")
    with io.open(path, "w") as f:
        f.write(str(CollectionLevel))

    path = os.path.join(topdir, "Stats\current_rank_cubes.txt")
    with io.open(path, "w") as f:
        f.write(str(RankCubes))

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
    # Collection level !cl followed by a number
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cl" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            commandsplit = data.Message.split(" ")
            CollectionLevel = int(commandsplit[1])
            path = os.path.join(topdir, "Stats\collection_level.txt")
            with io.open(path, "w") as f:
                f.write(str(CollectionLevel))
            Parent.SendStreamMessage("Collection level updated")

        except:
            Parent.SendStreamMessage("Failed to set collection level")

    if data.IsChatMessage() and data.GetParam(0).lower() == "!snapreset" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            path = os.path.join(topdir, "Stats\cubes_today.txt")
            with io.open(path, "w") as f:
                f.write("0")

            path = os.path.join(topdir, "Stats\wins.txt")
            with io.open(path, "w") as f:
                f.write("0")

            path = os.path.join(topdir, "Stats\losses.txt")
            with io.open(path, "w") as f:
                f.write("0")

            Parent.SendStreamMessage("Daily Snap stats reset")

        except:
            Parent.SendStreamMessage("Reset failed")

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
        
    return

# Unload
def Unload():
    return

# Script Toggle
def ScriptToggled(state):
    return
