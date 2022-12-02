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
    global LastCommand

    #Backups for undo
    global OldCubesToday
    
    global OldCurrentRank
    
    global OldCollectionLevel
    
    global OldHighestRank
    
    global OldWins
    
    global OldLosses
    
    global OldRankCubes

    # Collection level !cl followed by a number
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cl" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount = int(commandsplit[1])
            #backup
            OldCollectionLevel = CollectionLevel

            #set collection level
            CollectionLevel = msgAmount

            Write()
            LastCommand = data
            Parent.SendStreamMessage("Collection level updated")

        except:
            Parent.SendStreamMessage("Failed to set collection level")

    # Cubes added
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cubes+" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ") 
            msgAmount = int(commandsplit[1])
            if msgAmount == 1 or msgAmount == 2 or msgAmount == 4 or msgAmount == 8:
                #backup
                OldRankCubes = RankCubes
                OldCurrentRank = CurrentRank
                OldHighestRank = HighestRank
                OldCubesToday = CubesToday
                OldWins = Wins

                # Increase cubes and win
                CubesToday += msgAmount
                Wins += 1

                # Check for rank up/add cubes and/or rank
                if RankCubes + msgAmount >= 10:
                    RankCubes = RankCubes + msgAmount - 10
                    CurrentRank += 1
                else:
                    RankCubes += msgAmount
                
                # Check for new rank category
                if CurrentRank > HighestRank:
                    HighestRank = CurrentRank
                    if HighestRank % 10 == 0:
                        CurrentRank +=1
                        HighestRank +=1

                # saves changes
                Write()
                LastCommand = data

                Parent.SendStreamMessage("Stats updated")
            
            else:
                Parent.SendStreamMessage("Not a Valid number")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    # Cubes removed
    if data.IsChatMessage() and data.GetParam(0).lower() == "!cubes-" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ") 
            msgAmount = int(commandsplit[1])
            if msgAmount == 1 or msgAmount == 2 or msgAmount == 4 or msgAmount == 8:
            
                #backup
                OldRankCubes = RankCubes
                OldCurrentRank = CurrentRank
                OldHighestRank = HighestRank
                OldCubesToday = CubesToday
                OldLosses = Losses
                
                #decreases cubes and losses
                CubesToday -= msgAmount
                Losses += 1

                # Check for rank down/remove cubes and/or rank
                if RankCubes - msgAmount < 0:
                    RankCubes = RankCubes - msgAmount + 10
                    CurrentRank -= 1
                else:
                    RankCubes -= msgAmount
                    
                #saves changes
                Write()
                LastCommand = data

                Parent.SendStreamMessage("Stats updated")
            else:
                Parent.SendStreamMessage("Not a Valid number")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    # Reset command !snapreset resets daily cubes, wins, and losses
    if data.IsChatMessage() and data.GetParam(0).lower() == "!snapreset" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        #backup
        OldCubesToday = CubesToday
        OldLosses = Losses
        OldWins = Wins
        
        try:
            Reset()
            LastCommand = data
            Parent.SendStreamMessage("Daily Snap stats reset")

        except:
            Parent.SendStreamMessage("Reset failed")

    # Undo
    if data.IsChatMessage() and data.GetParam(0).lower() == "!undo" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            Undo()

            #saves changes
            Write()
            LastCommand = " "

            Parent.SendStreamMessage("Last SnapStats action undone")

        except:
            Parent.SendStreamMessage("Couldn't undo")
    
    return

# Undo method
def Undo():
    #global variables
    global CubesToday
    global CurrentRank
    global CollectionLevel
    global HighestRank
    global Wins
    global Losses
    global RankCubes
    global LastCommand

    if LastCommand.GetParam(0).lower() == "!cl":
        CollectionLevel = OldCollectionLevel

    if LastCommand.GetParam(0).lower() == "!snapreset":
        CubesToday = OldCubesToday
        Wins = OldWins
        Losses = OldLosses
    
    if LastCommand.GetParam(0).lower() == "!cubes+":
        CubesToday = OldCubesToday
        Wins = OldWins
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes

    if LastCommand.GetParam(0).lower() == "!cubes":
        CubesToday = OldCubesToday
        Losses = OldLosses
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes
        
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
