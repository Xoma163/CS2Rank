# CS2Rank

## Getting players rank in cs2 by auth and share codes

### Requirements:

1) Windows 10
2) Python3

### QUICK START
1) Get steam_key for API [here](https://steamcommunity.com/dev/apikey)
2) Create file `.env` and fill it like example file `.env.example`
3) Get your steam id: [help.steampowered.com](https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC) or [steamid.io](https://steamid.io/)
4) Get your auth and share codes [help.steampowered.com](https://help.steampowered.com/en/wizard/HelpWithGameIssue/?appid=730&issueid=128)
5) Create file `users.json` and fill it like example file `users.json.example`
6) `pip install -r requirements.txt`
7) `python main.py`

### How it works?

1) Find out the last match share code using Steam API. [Learn more](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Access_Match_History)
2) Decode share code with ShareCodeWorker. [Source](https://github.com/akiver/csgo-sharecode/blob/main/src/index.ts)
3) Find out the url for .dem file via [boiler-writter](https://github.com/akiver/boiler-writter/releases/tag/v1.4.0)
4) Download .dem and analyze it via [demoparser2](https://github.com/LaihoE/demoparser)
5) Save last share code to users.json
6) ???
7) PROFIT

### Known bugs
1) If a player quits the game, the script cannot understand whether he won or lost.
