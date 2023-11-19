import os
import subprocess

BOILER_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), 'boiler-writter.exe')


def do(file, match_id, outcome_id, token_id):
    command = f"{BOILER_PATH} {file} {match_id} {outcome_id} {token_id}"
    subprocess.check_output(
        command,
        stderr=subprocess.STDOUT,
        shell=True
    )
