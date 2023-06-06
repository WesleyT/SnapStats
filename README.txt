===================================================================
			SNAP STATS
			by Weazol
			  v 2.5
===================================================================

SETUP

Follow streamlabs guide to setup scripts in Streamlabs Chatbot.
https://streamlabs.com/content-hub/post/chatbot-scripts-desktop

Import this script
(in scripts tab, top right corner, second icon)

Set your current stats

Create live text in OBS or a static image with the titles of each 
stat you want to display.
I have included a shitty paint example.

Then for each stat you want to display in obs add a text source
and link it to the .txt file in the Stats folder.

---------
COMMANDS (all can be changed in settings)
---------

SNAPSTATS
The bot will put your stats in chat if you type
!snapstats

UNDO
Any command here can be undone with
!undo
This will only undo the last command that was done

COLLECTION LEVEL
To change your collection level do
!cl #
Where # is the current level
!cl 1389
Would set a collection level of 1389

VICTORY
Cubes and rank are adjusted together
!cubes+ #
Where # is how many cubes 1,2,4,or 8
!cubes+ 8
Would add 8 cubes and check if a rank needs to be added as well
NOTE. If you change cubes+ command make sure it is not similar to setcubes or cubes-

DEFEAT/ESCAPE
Cubes and rank are adjusted together
!cubes- #
Where # is how many cubes 1,2,4,or 8
!cubes- 8
Would remove 8 cubes and check if a rank needs to be removed as well
NOTE. If you change cubes- command make sure it is not similar to setcubes or cubes+

DAILY STATS
Your daily stats are tracked automatically with !cubes+ and !cubes-
RESET
To reset them each day
!snapreset
This will bring Wins, Losses, and Cubes Today to 0

NEW SEASON
The highest rank is calculated for cube gains.
Make sure to tell the bot when there is a new season using
!newseason

FIXES
If something goes wrong and !undo cant fix it.
You can manually adjust stats using these
!setwins #
where # is the number of wins
!setlosses #
where # is the number of losses
!setcubes #
where # is the total number for todays cubes
NOTE. If you change setcubes command make sure it is not similar to cubes- or cubes+

!sethighestrank #
Where # is the highest rank you have reached this season
!setrank # #
Where # # is the current rank and cubes in that rank
Ex
!rank 89 8
Would set a rank of 89 with 8 cubes

