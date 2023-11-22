import os

import requests


class SteamAPI:
    SHARE_CODE_URL = "https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1"
    API_KEY = os.getenv("STEAM_API_KEY")

    def get_last_game_code(self, code: str, steam_id: int, auth_code: str) -> str:
        params = {
            "key": self.API_KEY,
            "steamid": steam_id,
            "steamidkey": auth_code,
        }
        while code != "n/a":
            params['knowncode'] = code
            r = requests.get(self.SHARE_CODE_URL, params=params)
            r.raise_for_status()
            code = r.json()['result']['nextcode']

        code = params['knowncode']
        return code
