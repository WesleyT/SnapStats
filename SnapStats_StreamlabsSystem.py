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

    #   Create Stats Files with default or entered settings (will not overwrite)
    #   Also creates global variables while checking if files are created
    path = os.path.join(topdir, "Stats\current_rank.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["CurrentRank"]))
    with io.open(path, "r") as f:
        global CurrentRank
        CurrentRank = int(f.read())
    Parent.Log(ScriptName,"Rank is set at "+str(CurrentRank))
    
    path = os.path.join(topdir, "Stats\highest_rank.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["HighestRank"]))
    with io.open(path, "r") as f:
        global HighestRank
        HighestRank = int(f.read())
    Parent.Log(ScriptName,"Highest Rank is set at "+str(HighestRank))

    path = os.path.join(topdir, "Stats\collection_level.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["CollectionLevel"]))
    with io.open(path, "r") as f:
        global CollectionLevel
        CollectionLevel = int(f.read())
    Parent.Log(ScriptName,"Collection Level is set at "+str(CollectionLevel))

    path = os.path.join(topdir, "Stats\current_rank_cubes.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["RankCubes"]))
    with io.open(path, "r") as f:
        global RankCubes
        RankCubes = int(f.read())
    Parent.Log(ScriptName,"Cubes in current rank is set at "+str(RankCubes))

    path = os.path.join(topdir, "Stats\cubes_today.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")
    with io.open(path, "r") as f:
        global CubesToday
        CubesToday = int(f.read())
    Parent.Log(ScriptName,"Cubes Today is set at "+str(CubesToday))

    path = os.path.join(topdir, "Stats\wins.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")
    with io.open(path, "r") as f:
        global Wins
        Wins = int(f.read())
    Parent.Log(ScriptName,"Wins is set at "+str(Wins))

    path = os.path.join(topdir, "Stats\losses.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write("0")
    with io.open(path, "r") as f:
        global Losses
        Losses = int(f.read())
    Parent.Log(ScriptName,"Losses is set at "+str(Losses))

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

    # Reset command !snapreset resets daily cubes, wins, and losses
    if data.IsChatMessage() and data.GetParam(0).lower() == "!snapreset" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            Reset()
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

# Saves currently entered values to stats
def Save():

    try:
        with io.open(os.path.join(topdir, settingsFile), encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8-sig")

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

    except:
        Parent.Log(ScriptName, "Save Failed")
    
    return

# Reload/Save Settings
def ReloadSettings(jsonData):

    Save()
    Init()

    return

# Resets daily stats
def Reset():
    path = os.path.join(topdir, "Stats\cubes_today.txt")
    with io.open(path, "w") as f:
        f.write("0")

    path = os.path.join(topdir, "Stats\wins.txt")
    with io.open(path, "w") as f:
        f.write("0")

    path = os.path.join(topdir, "Stats\losses.txt")
    with io.open(path, "w") as f:
        f.write("0")    

    return

# Unload
def Unload():
    return

# Script Toggle
def ScriptToggled(state):

    if state:
        Init()

    return
