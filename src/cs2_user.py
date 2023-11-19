from src.match import Match
from src.utils.steam_api import SteamAPI


class CS2User:

    def __init__(self, steam_id: int, auth_code: str, share_code: str):
        self.steam_id: int = steam_id if isinstance(steam_id, int) else int(steam_id)
        self.auth_code: str = auth_code
        self.rank: int = 0

        self.last_match = Match(share_code=share_code)
        self.steam_api = SteamAPI()

    def _set_latest_match(self):
        code = self.steam_api.get_last_game_code(self.last_match.share_code, self.steam_id, self.auth_code)
        self.last_match = Match(code)

    def set_rank(self):
        self._set_latest_match()
        self.last_match.download_dem()
        self.rank = self.last_match.get_rank_after_game(self.steam_id)
