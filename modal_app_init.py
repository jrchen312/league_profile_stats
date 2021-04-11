import json


def appStarted(app):
    app.setActiveMode(app.searchScreenMode)
    app.timerDelay = 50
    app.currMatch = 0

    # Try to load in the API information:
    fileName = "settings.txt"
    try:
        with open(fileName) as json_file:
            info = json.load(json_file)
    except:
        info = None
        raise ("Existing match history not found!")
    app.api = info['api']
    app.seasonStart = info['seasonStart'] #time of start of season 11
    #
    #
    app.summonerInfo = dict()
    app.matchInfo = None
    app.resetEverything = False
    app.champIdToName = None