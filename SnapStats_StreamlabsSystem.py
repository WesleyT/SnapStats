import os
import json
import io
import math

#Script Info
ScriptName = "Snap Stats"
Website = "https://www.weazol.com"
Description = "A Script to assist with displaying snap stats in OBS"
Creator = "Weazol"
Version = "2.0"

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
            "Username": "",
            "StatsCommand": "!snapstats",
            "UndoCommand": "!undo",
            "CLCommand": "!cl",
            "VictoryCommand": "!cubes+",
            "DefeatCommand": "!cubes-",
            "ResetCommand": "!snapreset",
            "SeasonCommand": "!newseason",
            "SetWinsCommand": "!setwins",
            "SetLossesCommand": "!setlosses",
            "SetCubesCommand": "!setcubes",
            "SetHighestRankCommand": "!sethighestrank",
            "SetRankCommand": "!setrank"
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

    # report snap stats
    if data.IsChatMessage() and data.GetParam(0).lower() == settings["StatsCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):

        #checks for whisper else it sends to stream
        if data.IsWhisper():
            Parent.SendStreamWhisper(data.User, "Current Rank is " + str(CurrentRank) + " and " + str(RankCubes) + " cubes")
            Parent.SendStreamWhisper(data.User,"Today's Stats are " + str(Wins) + " wins and " + str(Losses) + " losses with a total of " + str(CubesToday) +" cubes")
            Parent.SendStreamWhisper(data.User,"Highest Rank achieved is " + str(HighestRank))
            Parent.SendStreamWhisper(data.User, "Collection Level is " + str(CollectionLevel))
        else:
            Parent.SendStreamMessage("Current Rank is " + str(CurrentRank) + " and " + str(RankCubes) + " cubes")
            Parent.SendStreamMessage("Today's Stats are " + str(Wins) + " wins and " + str(Losses) + " losses with a total of " + str(CubesToday) +" cubes")
            Parent.SendStreamMessage("Highest Rank achieved is " + str(HighestRank))
            Parent.SendStreamMessage("Collection Level is " + str(CollectionLevel))

    # Collection level !cl followed by a number
    if data.IsChatMessage() and data.GetParam(0).lower() == settings["CLCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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

            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Collection level updated")
            else:
                Parent.SendStreamMessage("Collection level updated")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set collection level")
            else:
                Parent.SendStreamMessage("Failed to set collection level")

    # Rank !setrank followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SetRankCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
            
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Rank updated")
            else:
                Parent.SendStreamMessage("Rank updated")

        except:
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set rank")
            else:
                Parent.SendStreamMessage("Failed to set rank")

    # Wins !setwins followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SetWinsCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
             #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Wins updated")
            else:
                Parent.SendStreamMessage("Wins updated")

        except:
             #checks for whisper else it sends to stream
            if data.IsWhisper():    
                Parent.SendStreamWhisper(data.User, "Failed to set wins")
            else:
                Parent.SendStreamMessage("Failed to set wins")

    # Losses !setlosses followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SetLossesCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
            
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Losses updated")
            else:
                Parent.SendStreamMessage("Losses updated")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set losses")
            else:
                Parent.SendStreamMessage("Failed to set losses")

    # Todays cubes !setcubes followed by a number
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SetCubesCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Cubes updated")
            else:
                Parent.SendStreamMessage("Cubes updated")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set cubes")
            else:
                Parent.SendStreamMessage("Failed to set cubes")

    # Highestrank (for fixes only)
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SetHighestRankCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Highest Rank updated")
            else:
                Parent.SendStreamMessage("Highest Rank updated")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set Highest Rank")
            else:
                Parent.SendStreamMessage("Failed to set Highest Rank")

    # New season
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["SeasonCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            #backup
            OldHighestRank = HighestRank
            OldCurrentRank = CurrentRank
            OldRankCubes = RankCubes

            CurrentRank = math.trunc(math.floor((CurrentRank - 30) / 10) * 10)
            if CurrentRank < 10:
                CurrentRank = 10
            if CurrentRank > 70:
                CurrentRank = 70
            HighestRank = CurrentRank
            RankCubes = 0

            Write()
            LastCommand = data
            UndidCommand = " "
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "New snap season! rank updated")
            else:
                Parent.SendStreamMessage("New snap season! rank updated")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to set rank")
            else:
                Parent.SendStreamMessage("Failed to set rank")

    # Cubes added
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["VictoryCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
                    # gives extra level for ever 10 levels under 100
                    if HighestRank % 10 == 0 and HighestRank < 101:
                        CurrentRank +=1
                        HighestRank +=1

                # saves changes
                Write()
                UndidCommand = " "
                LastCommand = data
                #checks for whisper else it sends to stream
                if data.IsWhisper():
                    Parent.SendStreamWhisper(data.User, "Stats updated")
                else:
                    Parent.SendStreamMessage("Stats updated")
            
            else:
                #checks for whisper else it sends to stream
                if data.IsWhisper():
                    Parent.SendStreamWhisper(data.User, "Not a Valid number")
                else:
                    Parent.SendStreamMessage("Not a Valid number")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to update stats")
            else:
                Parent.SendStreamMessage("Failed to update stats")

    # Cubes removed
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["DefeatCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
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
                    if CurrentRank != 10 and CurrentRank != 100:
                        CurrentRank -= 1
                    else: RankCubes = 0 
                else:
                    RankCubes -= msgAmount
                    
                #saves changes
                Write()
                UndidCommand = " "
                LastCommand = data

                #checks for whisper else it sends to stream
                if data.IsWhisper():
                    Parent.SendStreamWhisper(data.User, "Stats updated")
                else:
                    Parent.SendStreamMessage("Stats updated")
            else:
                #checks for whisper else it sends to stream
                if data.IsWhisper():
                    Parent.SendStreamWhisper(data.User, "Not a Valid number")
                else:
                    Parent.SendStreamMessage("Not a Valid number")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Failed to update stats")
            else:
                Parent.SendStreamMessage("Failed to update stats")

    # Reset command !snapreset resets daily cubes, wins, and losses
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["ResetCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        #backup
        OldCubesToday = CubesToday
        OldLosses = Losses
        OldWins = Wins
        
        try:
            Reset()
            UndidCommand = " "
            LastCommand = data
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Daily Snap stats reset")
            else:
                Parent.SendStreamMessage("Daily Snap stats reset")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Reset failed")
            else:
                Parent.SendStreamMessage("Reset failed")

    # Undo
    elif data.IsChatMessage() and data.GetParam(0).lower() == settings["UndoCommand"] and Parent.HasPermission(data.User,settings["Permission"],settings["Username"]):
        try:
            Undo()
            #saves changes
            Write()
            
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Last SnapStats action undone")
            else:
                Parent.SendStreamMessage("Last SnapStats action undone")

        except:
            #checks for whisper else it sends to stream
            if data.IsWhisper():
                Parent.SendStreamWhisper(data.User, "Couldn't undo")
            else:
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

    elif LastCommand.GetParam(0).lower() == settings["CLCommand"]:
        CollectionLevel = OldCollectionLevel
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == settings["ResetCommand"]:
        CubesToday = OldCubesToday
        Wins = OldWins
        Losses = OldLosses
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == settings["VictoryCommand"]:
        CubesToday = OldCubesToday
        Wins = OldWins
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == settings["DefeatCommand"]:
        CubesToday = OldCubesToday
        Losses = OldLosses
        CurrentRank = OldCurrentRank
        HighestRank = OldHighestRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == settings["SetRankCommand"]:
        CurrentRank = OldCurrentRank
        RankCubes = OldRankCubes
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == settings["SetCubesCommand"]:
        CubesToday = OldCubesToday
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == settings["SetWinsCommand"]:
        Wins = OldWins
        UndidCommand = LastCommand
    
    elif LastCommand.GetParam(0).lower() == settings["SetLossesCommand"]:
        Losses = OldLosses
        UndidCommand = LastCommand

    elif LastCommand.GetParam(0).lower() == settings["SeasonCommand"]:
        HighestRank = OldHighestRank
        CurrentRank = OldCurrentRank

    elif LastCommand.GetParam(0).lower() == settings["SetHighestRankCommand"]:
        HighestRank = OldHighestRank 

    return

# Tick method 
def Tick():
    return

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