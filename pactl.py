import re
import subprocess


def list_sinks_string() -> str:
    return subprocess.run(['pactl', 'list', 'sinks'], capture_output=True).stdout.decode()


def split_sinks_string(all_sinks: str) -> list[str]:
    return re.split(r'Sink #\d+', all_sinks)[1:]


def regex_match_one(pattern: str | re.Pattern[str], string: str) -> str:
    result = re.search(pattern, string, re.I)
    if result and len(result.groups()) == 1:
        return result.groups()[0]


def get_sink_string_attribute(sink: str, attr: str) -> str | None:
    return regex_match_one(rf'\n\s+{attr}: ([^\n]+)', sink)


def get_sink_string_property(sink: str, prop: str) -> str | None:
    return regex_match_one(rf'\n\s+{prop} = "([^\n]+)"\n', sink)


class Sink:
    def __init__(self, sink_data: str):
        self.name = get_sink_string_attribute(sink_data, 'Name')
        self.description = get_sink_string_attribute(sink_data, 'Description')
        self.mute = get_sink_string_attribute(sink_data, 'Mute') != 'no'
        self.current = get_sink_string_attribute(sink_data, 'State') == 'RUNNING'

    def __str__(self) -> str:
        return self.description or self.name or "No sink data available"

    @property
    def default_command(self):
        return f"pactl set-default-sink {self.name}"


def parse_all_sinks() -> list[Sink]:
    return list(map(Sink, split_sinks_string(list_sinks_string())))
