import subprocess


def list_sinks():
    return subprocess.run(['pactl', 'list', 'sinks'], capture_output=True).stdout.decode()
