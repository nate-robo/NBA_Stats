import nbastats.nbastats as nbastats

class playerStats:

    def __init__(self, nameIn, effIn, playerIdIn, teamIn):
        self.name = nameIn
        self.EFF = effIn
        self.playerID = playerIdIn
        self.team = teamIn
        self.gameList = []
        self.totalPM = 0
        self.gamePM = 0


    def getGames(self):
        gameLog = nbastats.GameLog(self.playerID).log()
        gameLog = gameLog.reindex(columns=['Game_ID','MATCHUP'])
        games = gameLog.get_values()
        gamesArray = []
        count = 0
        for game in games:
            gamesArray.append([game[0]])
            ''' UNCOMMENT TO ADD BOOLEAN FLAG FOR IF STARTING OR NOT
            matchUp = game[1].split(' ')
            if matchUp [1] == 'vs.':
                gamesArray[count].append(True) #game is home
            else:
                gamesArray[count].append(False) #game is away
            count += 1
            '''
        self.gameList = gamesArray


if __name__=='__main__':

    #player = playerStats('Kevin Love', 40.0, 201567, 'MIN')
    #games = player.getGames()
    #player = playerStats('John Wall', '27.3', '202322', 'WAS')

    '''
    for game in games:
        player.testPM(game[0], game[1])
    '''
    #player.testPM()


