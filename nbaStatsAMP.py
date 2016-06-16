"""
nbaStatsAMP.py
--------------------------------------
Nathan Robinson
Last Modified: 4/13/2015
--------------------------------------
NBA STATS AMP:
    nbaStatsAMP is a program performs a ranking comparison using statistical analysis between
    two methods of quantifying individual player contributions to producing wins within the NBA.
    This analysis is based off the 2013/14, 2014/15 Regular Seasons in the NBA.The most typically
    used method: (EFF) data for the 2013 season has major drawbacks as it
    only accounts for box score stats while not any non-stat sheet actions. In comparison Adjusted
    Plus Minus (APM) incorporates a more holistic approach. APM will seek to provide a more
    accurate ranking of players that viewers/fans/critics perceived to be the best players in the NBA.
    I'm using the nbastats 1.1 library to retrieve the information from the official NBA stats
    in combination with the pandas
--------------------------------------
"""
# TODO : Unit Testing
# TODO : Function Comments
# TODO : Create text-based UI
# TODO : Incorporate RAPM method

#IMPORTS
import nbastats.nbastats as nbastats
from NBA_Stats import playerStats
from math import floor

class nbaPlayerAMP:

    def __init__(self):
        self.playerList = [] #List of playerLists --> [PLAYER_NAME, EFF, PLAYER_ID, TEAM, ...]
        self.playerObjList = [] #List of playerStats Objects
        self.gamesDict = {}


    def writeBestPlayers(self):
        """
        Get best players from 2013/14 Season from nbaStats module, ranking by EFF (Efficiency)
        and write the ranking to file -> PLAYERNAME, EFF per player
        :return: NONE; ranking of players written to file in data/playerEFF.txt
        """
        leagueLeaders = nbastats.LeagueLeaders(season='2013-14')
        leaders = leagueLeaders.line()
        reIndex = leaders.reindex(columns=['PLAYER','EFF','PLAYER_ID','TEAM']) #Only retrieve the player names and their EFF (efficiency)
        reIndex = reIndex.sort(columns=['EFF'], ascending = False)
        print(reIndex)
        reIndex.to_csv('data/playerEFF.txt', columns=['PLAYER','EFF','PLAYER_ID','TEAM'], index=False, mode='w') #Write ranking to textfile

    def writeGameIDs(self):
        filePath = 'data/gameIDs.txt'
        file = open(filePath, 'w', encoding='utf-8')
        gameIDs = self.gamesDict.keys()
        for gameID in gameIDs:
            file.write(gameID+'\n')

        file.close()

    def getBestPlayers(self):
        """
        Parse text file containing best players based of EFF and append the top 30 players to an array of arrays.
        This array will be used as the set of players compared in the analysis with extra neccesary info.
        :return: Array of Top 30 Players from 13/14 Season, each player in the array contains array of PLAYER_NAME,EFF,PLAYER_ID,TEAM
        """
        filePath = 'data/playerEFF.txt'
        f = open(filePath, 'r+', encoding='utf-8')
        lines = f.readlines()
        counter = 0
        for line in lines:
            if len( self.playerList ) < 30:
                cleanLine = line.strip('\n')
                cleanLine = cleanLine.split(',')
                if cleanLine[0] != 'PLAYER': #Don't write first table header value to file
                    self.playerList.append(cleanLine)
                    counter += 1
        f.close()

    def getPlayerGames(self, playerID):
        """
        Uses the player ID to query for all the ShotChart data for the regular season.
        look through this data focusing on the GAME_ID column and append the game ID to the gamesPlayed array
        if it doesn't already exist in the array effectively retrieving a set of all games the player participated in
        :param playerID: id of player for NBA stats
        :return: gamesPlayed: all regular season games the player participated in.
        """

        shotChart = nbastats.ShotChart(playerID).shotchart()
        gameIDs = shotChart.reindex(columns=['GAME_ID']) #Eliminate irrelevant info returned from shotchart, only look at gameIDs
        idList = gameIDs.get_values() #Retreive numpy array from dataframe object
        count = 0
        gamesPlayed = []

        for game in idList:
            if game[0] not in gamesPlayed:
                gamesPlayed.append(idList[count][0])
            count += 1
        print(gamesPlayed)
        return gamesPlayed


    def parsePBP(self):
        """ ROUGH ABLE TO RETREIVE PLAY BY PLAY DATA, UNABLE TO USE WITHOUT MONITORING OFF THE CLOCK SUBS
        print("In main: before playByPlay")
        playByPlay = nbastats.PlayByPlay('0021300001').pbp()
        #print('This is a datafrmame: ', playByPlay._xs)
        modify = playByPlay.reindex(columns=['EVENTNUM', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION'])
        print(modify)
        print('This should not be a dataframe: ', playByPlay)
        print(playByPlay.lookup(row_labels = [10], col_labels = ['HOMEDESCRIPTION']))

        print(modify.get_values())
        eventArray = modify.get_values()
        print(eventArray[0][2])

        """

    def createPlayersToGames(self):
        """
        Creates main data structure for use throughout program which is just a dictionary of
        gameIDs to player object arrays. For each game there is an array of a certain # of players
        who participated in said game.
        :return: None, creates main data structure --> gamesDict
        """
        for player in self.playerList:
            playerObj = playerStats.playerStats(player[0],player[1],player[2],player[3])
            playerObj.getGames()
            self.playerObjList.append(playerObj)
            #print(playerObj.name, ' : ', len(playerObj.gameList))
            for game in playerObj.gameList:
                if game[0] not in self.gamesDict:
                    self.gamesDict[game[0]] = [playerObj]
                else:
                    self.gamesDict[game[0]].append(playerObj)


    def calcTotalPM(self):
        """
        Goes through every game in the gameList set, gets all the players who participated in that game and
        then adds the player (+,-) val from the boxscore to the player's running total. Then write the players
        info to file for use in calculating the final eval on plus minus. This includes writing the playerName,
        playerTotalPM score, and the number of games the player participated in.
        :param: None
        :return: None, writes to a file
        """

        for game in self.gamesDict:
            playersForGame = self.gamesDict[game] #Get all players in my set that participated in the game
            box = nbastats.BoxScore(game).playerstats().reindex(columns=['PLAYER_ID', 'PLUS_MINUS'])
            plusMinusVals = box.get_values()
            for val in plusMinusVals:
                for player in playersForGame:
                    if int(player.playerID) == val[0]:
                        player.totalPM += val[1]
                        print(player.name, ': ', player.totalPM)

        filePath = 'data/totalPM.txt'
        f = open(filePath, 'w+', encoding='utf-8')
        for player in self.playerObjList:
            f.write(player.name + ',' + player.totalPM + ',' + len(player.gameList)+'\n')
        f.close()

    def getNumPlayersGames(self):
        """
        Prints the players name and the # of games they played in for the season, used for debugging/info purposes
        :return: None
        """
        for player in self.playerObjList:
            print(player.name, ":" , len(player.gameList))

    def rankPerGamePM(self):
        """
        Uses the file generated from calcTotalPM to get the per-game (+,-) by dividing each players
        total(+,-) by the number of games they participated in. Then reranks based off their per-game
        to create the desired hierarchy / outcome.
        NOTE: In future will use internal data structures to get my ranking versus uisng file IO, the
        info is readily available within my player objects and could avoid the I/O bottleneck
        :return: None, prints ranking to console
        """
        filePath = 'data/totalPM.txt'
        f = open(filePath, 'r+', encoding='utf-8')
        lines = f.readlines()
        counter = 0
        bestPlayers = []
        for line in lines:
            cleanLine = line.strip('\n')
            cleanLine = cleanLine.split(',')
            print(cleanLine)
            pmRating = int(float(cleanLine[1]))/int(cleanLine[2])
            print(pmRating)
            bestPlayers.append([cleanLine[0],pmRating])
            counter += 1
        f.close()

        bestPlayers = sorted(bestPlayers, key=lambda x: x[1], reverse=True)
        for player in bestPlayers:
            print(player[0], '%0.3f' % player[1])

    def rankByPM(self): #Should remove later
        self.playerObjList.sort(key=lambda x: x.totalPM, reverse=True)
        for player in self.playerObjList:
            print(player.name, ' : ' , player.totalPM)


if __name__=='__main__':
    stats = nbaPlayerAMP()
    stats.writeBestPlayers()
    stats.getBestPlayers()

    stats.createPlayersToGames()
    stats.calcTotalPM()
    stats.getNumPlayersGames()
    stats.rankPerGamePM()


