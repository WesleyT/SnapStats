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
    
    #global variables
    global CubesToday
    global CurrentRank
    global CollectionLevel
    global HighestRank
    global Wins
    global Losses
    global RankCubes

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

    # Cubes added
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cubes+" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            commandsplit = data.Message.split(" ") 
            CubesToday += int(commandsplit[1])
            Wins += 1

            # Check for rank up
            if RankCubes + int(commandsplit[1]) >= 10:
                RankCubes = RankCubes + int(commandsplit[1]) - 10
                CurrentRank += 1
            else:
                RankCubes += int(commandsplit[1])
            
            # Check for new rank category
            if CurrentRank > HighestRank:
                HighestRank = CurrentRank
                if HighestRank % 10 == 0:
                    CurrentRank +=1
                    HighestRank +=1

            Write()

            Parent.SendStreamMessage("Stats updated")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    # Cubes removed
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cubes-" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            commandsplit = data.Message.split(" ") 
            CubesToday -= int(commandsplit[1])
            Losses += 1

            # Check for rank up
            if RankCubes - int(commandsplit[1]) < 0:
                RankCubes = RankCubes - int(commandsplit[1]) + 10
                CurrentRank -= 1
            else:
                RankCubes -= int(commandsplit[1])
                
            Write()
            
            Parent.SendStreamMessage("Stats updated")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    return
# Tick method 
def Tick():
    return

#unused Parse method
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

def Write():
    # Write new stats to files
    path = os.path.join(topdir, "Stats\cubes_today.txt")
    with io.open(path, "w") as f:
        f.write(str(CubesToday))

    path = os.path.join(topdir, "Stats\current_rank_cubes.txt")
    with io.open(path, "w") as f:
        f.write(str(RankCubes))

    path = os.path.join(topdir, "Stats\collection_level.txt")
    with io.open(path, "w") as f:
        f.write(str(CollectionLevel))

    path = os.path.join(topdir, "Stats\current_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(CurrentRank))

    path = os.path.join(topdir, "Stats\highest_rank.txt")
    with io.open(path, "w") as f:
        f.write(str(HighestRank))

    path = os.path.join(topdir, "Stats\wins.txt")
    with io.open(path, "w") as f:
        f.write(str(Wins))

    path = os.path.join(topdir, "Stats\losses.txt")
    with io.open(path, "w") as f:
        f.write(str(Losses))     

    return

# Saves currently entered values to stats
def Save():
    global CurrentRank
    global HighestRank
    global CollectionLevel
    global RankCubes
    global settings

    try:
        with io.open(os.path.join(topdir, settingsFile), encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8-sig")

        CurrentRank = settings["CurrentRank"]
        HighestRank = settings["HighestRank"]
        CollectionLevel = settings["CollectionLevel"]
        RankCubes = settings["RankCubes"]
        Write()

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
    global CubesToday
    global Wins
    global Losses

    path = os.path.join(topdir, "Stats\cubes_today.txt")
    with io.open(path, "w") as f:
        f.write("0")
    CubesToday = 0

    path = os.path.join(topdir, "Stats\wins.txt")
    with io.open(path, "w") as f:
        f.write("0")
    Wins = 0

    path = os.path.join(topdir, "Stats\losses.txt")
    with io.open(path, "w") as f:
        f.write("0")    
    Losses = 0

    return

# Unload
def Unload():
    return

# Script Toggle
def ScriptToggled(state):

    if state:
        Init()

    return
