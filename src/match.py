import os
import re
from bz2 import BZ2File

import requests
from demoparser2 import DemoParser
from pandas import DataFrame

from src.utils.boiler_writter import boiler


# https://github.com/akiver/csgo-sharecode/blob/main/src/index.ts
class Match:
    DICTIONARY = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789'
    DICTIONARY_LENGTH = len(DICTIONARY)

    DEM_URL_RE = "http:.*\.dem\.bz2"

    def __init__(self, share_code=None, match_id=None, outcome_id=None, token_id=None):
        self.share_code = share_code
        self.match_id = match_id
        self.outcome_id = outcome_id
        self.token_id = token_id

        if share_code:
            self.decode()
        elif match_id and outcome_id and token_id:
            self.encode()
        else:
            raise RuntimeError("share_code or match_id and outcome_id and token_id must be provided")

    @staticmethod
    def _bytes_to_hex(_bytes):
        return ''.join(format(byte, '02x') for byte in _bytes)

    def _bytes_to_big_int(self, _bytes):
        _hex = self._bytes_to_hex(_bytes)
        return int(_hex, 16)

    @staticmethod
    def _int16_to_bytes(number):
        return [(number & 0xff00) >> 8, number & 0xff]

    @staticmethod
    def _string_to_bytes(_str):
        _bytes = []
        for i in range(0, len(_str), 2):
            byte = int(_str[i:i + 2], 16)
            _bytes.append(byte)
        return _bytes

    def _share_code_to_bytes(self, share_code):
        share_code = share_code.replace('CSGO', '').replace('-', '')
        chars = list(share_code)[::-1]
        big = 0
        for i in range(len(chars)):
            big = big * self.DICTIONARY_LENGTH + self.DICTIONARY.index(chars[i])
        _str = hex(big)[2:].zfill(36)
        _bytes = self._string_to_bytes(_str)
        return _bytes

    def _bytes_to_share_code(self, _bytes):
        _hex = self._bytes_to_hex(_bytes)
        total = int(_hex, 16)
        chars = ''
        for _ in range(25):
            rem = total % self.DICTIONARY_LENGTH
            chars += self.DICTIONARY[rem]
            total = total // self.DICTIONARY_LENGTH
        return f'CSGO-{chars[:5]}-{chars[5:10]}-{chars[10:15]}-{chars[15:20]}-{chars[20:25]}'

    def encode(self):
        match_bytes = self._string_to_bytes(hex(self.match_id)[2:].zfill(16))[::-1]
        reservation_bytes = self._string_to_bytes(hex(self.outcome_id)[2:].zfill(16))[::-1]
        tv_bytes = self._int16_to_bytes(self.token_id)[::-1]
        _bytes = match_bytes + reservation_bytes + tv_bytes
        self.share_code = self._bytes_to_share_code(_bytes)

    def decode(self):
        _bytes = self._share_code_to_bytes(self.share_code)
        self.match_id = self._bytes_to_big_int(_bytes[:8][::-1])
        self.outcome_id = self._bytes_to_big_int(_bytes[8:16][::-1])
        self.token_id = self._bytes_to_big_int(_bytes[16:18][::-1])

    @property
    def info_file_path(self):
        return os.path.join("tmp", "match.info")

    @property
    def dem_archive_file_path(self):
        return os.path.join("tmp", f"{self.share_code}.dem.bz2")

    @property
    def dem_file_path(self):
        return os.path.join("tmp", f"{self.share_code}.dem")

    def download_dem(self):
        if os.path.exists(self.dem_file_path):
            return
        try:
            boiler.do(
                self.info_file_path,
                self.match_id,
                self.outcome_id,
                self.token_id
            )

            with open(self.info_file_path, 'r', encoding='utf8', errors="ignore") as file:
                content = file.read()
        finally:
            os.remove(self.info_file_path)

        r = re.compile(self.DEM_URL_RE)
        dem_archive_url = r.findall(content)[0]

        r = requests.get(dem_archive_url)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise RuntimeError(f"problem with getting dem archive {dem_archive_url}. Probably steam server error")

        with open(self.dem_archive_file_path, 'wb') as file:
            file.write(r.content)

        chunk_size = 100 * 1024
        with open(self.dem_file_path, 'wb') as out_file:
            with BZ2File(self.dem_archive_file_path, "r") as bz2_file:
                try:
                    for data in iter(lambda: bz2_file.read(chunk_size), b""):
                        out_file.write(data)
                except OSError:
                    print(f"problem with unzipping {self.dem_archive_file_path}")
                    os.remove(self.dem_file_path)
                    raise

    def get_rank_after_game(self, steam_id):
        parser = DemoParser(os.path.abspath(self.dem_file_path))
        max_tick = parser.parse_event("round_end")["tick"].max()

        wanted_fields = ["rank_if_win", "rank_if_loss", "rank_if_tie", "team_rounds_total", "player_steamid"]
        df: DataFrame = parser.parse_ticks(wanted_fields, ticks=[max_tick])

        max_state = int(df["team_rounds_total"].max())
        min_state = int(df["team_rounds_total"].min())

        player = df.loc[df['player_steamid'] == steam_id]

        # ToDo: if user leave we cant get info by this way
        try:
            player_won_rounds = int(player['team_rounds_total'].iloc[0])
        except ValueError:
            player_won_rounds = min_state
        if max_state == min_state:
            return int(player['rank_if_tie'].iloc[0])
        elif player_won_rounds == max_state:
            return int(player['rank_if_win'].iloc[0])
        elif player_won_rounds == min_state:
            return int(player['rank_if_loss'].iloc[0])
        else:
            print("is it possible")
