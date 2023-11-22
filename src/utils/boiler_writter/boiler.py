import os
import subprocess

BOILER_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), 'boiler-writter.exe')


def do(file, match_id, outcome_id, token_id):
    command = f"{BOILER_PATH} {file} {match_id} {outcome_id} {token_id}"
    try:
        subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True
        )
    except Exception as e:
        if e.args[0] == 4:
            raise RuntimeError("Close CS2 app")
        if e.args[0] == 6:
            raise RuntimeError("Start steam app")
        raise
