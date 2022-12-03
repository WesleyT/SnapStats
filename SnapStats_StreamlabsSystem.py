import os
import json
import io
import math

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
        pass
        settings = {
            "CollectionLevel": 50,
            "CurrentRank": 10,
            "RankCubes": 0,
            "HighestRank": 10,
            "Wins": 0,
            "Losses": 0,
            "CubesToday": 0,
            "Permission": "Moderator",
            "Username": ""
            }

    #   Create Stats Directory
    directory = os.path.join(topdir, "Stats")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Create Stats Files with default or entered settings (will not overwrite)
    #   Also creates global variables while checking if files are created
    #       This is to ensure global variables arent over written on accidental script reset
    #       Only pressing save settings or initial launch will rewrite files with whats typed in
    path = os.path.join(topdir, "Stats\current_rank.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["CurrentRank"]))
    with io.open(path, "r") as f:
        global CurrentRank
        CurrentRank = int(f.read())
    
    path = os.path.join(topdir, "Stats\highest_rank.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["HighestRank"]))
    with io.open(path, "r") as f:
        global HighestRank
        HighestRank = int(f.read())

    path = os.path.join(topdir, "Stats\collection_level.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["CollectionLevel"]))
    with io.open(path, "r") as f:
        global CollectionLevel
        CollectionLevel = int(f.read())

    path = os.path.join(topdir, "Stats\current_rank_cubes.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["RankCubes"]))
    with io.open(path, "r") as f:
        global RankCubes
        RankCubes = int(float(f.read()))

    path = os.path.join(topdir, "Stats\cubes_today.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["CubesToday"]))
    with io.open(path, "r") as f:
        global CubesToday
        CubesToday = int(f.read())

    path = os.path.join(topdir, "Stats\wins.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["Wins"]))
    with io.open(path, "r") as f:
        global Wins
        Wins = int(f.read())

    path = os.path.join(topdir, "Stats\losses.txt")
    if not os.path.exists(path):
        with io.open(path, "w") as f:
            f.write(str(settings["Losses"]))
    with io.open(path, "r") as f:
        global Losses
        Losses = int(f.read())

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

    #Backup variables
    global OldCubesToday
    global OldCurrentRank
    global OldCollectionLevel
    global OldHighestRank
    global OldWins
    global OldLosses
    global OldRankCubes
    global LastCommand
    global UndidCommand

    
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
            UndidCommand = " "
            Parent.SendStreamMessage("Collection level updated")

        except:
            Parent.SendStreamMessage("Failed to set collection level")

    # Rank !rank followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!rank" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount1 = int(commandsplit[1])
            if 0 <= int(commandsplit[2]) <= 9:
                msgAmount2 = int(commandsplit[2])
            
            #backup
            OldCurrentRank = CurrentRank
            OldRankCubes = RankCubes

            #set rank and cubes
            CurrentRank = msgAmount1
            RankCubes = msgAmount2

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("Rank updated")

        except:
            Parent.SendStreamMessage("Failed to set rank")

    # Wins !wins followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!wins" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount = int(commandsplit[1])
            #backup
            OldWins = Wins

            #set wins
            Wins = msgAmount

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("Wins updated")

        except:
            Parent.SendStreamMessage("Failed to set wins")

    # Losses !losses followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!losses" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount = int(commandsplit[1])
            
            #backup
            OldLosses = Losses

            #set losses
            Losses = msgAmount

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("Losses updated")

        except:
            Parent.SendStreamMessage("Failed to set losses")

    # Todays cubes !cubes followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!cubes" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount = int(commandsplit[1])
            
            #backup
            OldCubesToday = CubesToday

            #set cubes
            CubesToday = msgAmount

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("Cubes updated")

        except:
            Parent.SendStreamMessage("Failed to set cubes")

    # Highestrank (for fixes only)
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!hrank" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #Verifys an interger follows
            commandsplit = data.Message.split(" ")
            msgAmount = int(commandsplit[1])
            
            #backup
            OldHighestRank = HighestRank

            #set losses
            HighestRank = msgAmount

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("Highest Rank updated")

        except:
            Parent.SendStreamMessage("Failed to set Highest Rank")

    # New season
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!newseason" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #backup
            OldHighestRank = HighestRank
            OldCurrentRank = CurrentRank

            CurrentRank = math.trunc(math.floor((CurrentRank - 30) / 10) * 10)
            if CurrentRank < 10:
                CurrentRank = 10
            HighestRank = CurrentRank

            Write()
            LastCommand = data
            UndidCommand = " "
            Parent.SendStreamMessage("New snap season! rank updated")

        except:
            Parent.SendStreamMessage("Failed to set rank")

    # Cubes added
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!cubes+" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
                UndidCommand = " "
                LastCommand = data

                Parent.SendStreamMessage("Stats updated")
            
            else:
                Parent.SendStreamMessage("Not a Valid number")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    # Cubes removed
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!cubes-" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
                    if CurrentRank != 10 or CurrentRank != 100:
                        CurrentRank -= 1
                else:
                    RankCubes -= msgAmount
                    
                #saves changes
                Write()
                UndidCommand = " "
                LastCommand = data

                Parent.SendStreamMessage("Stats updated")
            else:
                Parent.SendStreamMessage("Not a Valid number")

        except:
            Parent.SendStreamMessage("Failed to update stats")

    # Reset command !snapreset resets daily cubes, wins, and losses
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!snapreset" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        #backup
        OldCubesToday = CubesToday
        OldLosses = Losses
        OldWins = Wins
        
        try:
            Reset()
            UndidCommand = " "
            LastCommand = data
            Parent.SendStreamMessage("Daily Snap stats reset")

        except:
            Parent.SendStreamMessage("Reset failed")

    # Undo
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!undo" and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            Undo()
            #saves changes
            Write()

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
    global UndidCommand

    if UndidCommand != " ":
        Execute(UndidCommand)

    elif LastCommand.GetParam(0).lower() == "!cl":
        CollectionLevel = OldCollectionLevel
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == "!snapreset":
        CubesToday = OldCubesToday
        Wins = OldWins
        Losses = OldLosses
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == "!cubes+":
        CubesToday = OldCubesToday
        Wins = OldWins
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == "!cubes-":
        CubesToday = OldCubesToday
        Losses = OldLosses
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == "!rank":
        CurrentRank = OldCurrentRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == "!cubes":
        CubesToday = OldCubesToday
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == "!wins":
        Wins = OldWins
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == "!losses":
        Losses = OldLosses
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == "!newseason":
        HighestRank = OldHighestRank
        CurrentRank = OldCurrentRank

    elif LastCommand.GetParam(0).lower() == "!hrank":
        HighestRank = OldHighestRank 

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
def SaveStats():
    global CurrentRank
    global HighestRank
    global CollectionLevel
    global RankCubes
    global settings
    global Wins
    global Losses
    global CubesToday

    try:
        with io.open(os.path.join(topdir, settingsFile), encoding="utf-8-sig", mode="r") as f:
            settings = json.load(f, encoding="utf-8-sig")

        CurrentRank = int(settings["CurrentRank"])
        HighestRank = int(settings["HighestRank"])
        CollectionLevel = int(settings["CollectionLevel"])
        RankCubes = int(float(settings["RankCubes"]))
        Wins = int(settings["Wins"])
        Losses = int(settings["Losses"])
        CubesToday = int(settings["CubesToday"])
        Write()

    except:
        Parent.Log(ScriptName, "Save Failed")
    
    return

# Reload/Save Settings
def ReloadSettings(jsonData):
    SaveStats()
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

# Readme
def ReadMe():
	info = os.path.join(topdir, "README.txt")
	os.startfile(info)
	return