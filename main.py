from dotenv import load_dotenv

load_dotenv()

import glob
import os.path
from typing import List

from src.cs2_user import CS2User
from src.utils.users import Users

TMP_PATH = 'tmp'


def main():
    uc = Users()

    # load users
    cs2_users: List[CS2User] = [CS2User(user, **uc.users[user]) for user in uc.users]
    ranks = []
    try:
        for user in cs2_users:
            user.set_rank()
            ranks.append(user.rank)

            uc.set_code(user.steam_id, user.last_match.share_code)

        print(ranks)

        # do something with this info
        avg_rank = sum(ranks) / len(ranks)
        print(avg_rank)
    finally:
        # save latest share codes
        uc.write()

        # clear tmp dir. delete this code if you need .dem files
        files = glob.glob(TMP_PATH + '/*')
        for f in files:
            if f == '.gitkeep':
                continue
            os.remove(f)


if __name__ == "__main__":
    main()
