import abc
import re
import subprocess


def list_nodes_string(node: str) -> str:
    return subprocess.run(['pactl', 'list', node], capture_output=True).stdout.decode()


def get_sink_strings() -> list[str]:
    return re.split(r'Sink #\d+', list_nodes_string('sinks'))[1:]


def get_source_strings() -> list[str]:
    return re.split(r'Source #\d+', list_nodes_string('sources'))[1:]


def regex_match_one(pattern: str | re.Pattern[str], string: str) -> str:
    result = re.search(pattern, string, re.I)
    if result and len(result.groups()) == 1:
        return result.groups()[0]


def get_attribute(sink: str, attr: str) -> str | None:
    return regex_match_one(rf'\n\s+{attr}: ([^\n]+)', sink)


def get_property(sink: str, prop: str) -> str | None:
    return regex_match_one(rf'\n\s+{prop} = "([^\n]+)"\n', sink)


class Node(abc.ABC):
    def __init__(self, sink_data: str):
        self.name = get_attribute(sink_data, 'Name')
        self.description = get_attribute(sink_data, 'Description')
        self.mute = get_attribute(sink_data, 'Mute') != 'no'
        self.current = get_attribute(sink_data, 'State') == 'RUNNING'

    def __str__(self) -> str:
        return self.description or self.name or "No sink data available"

    @property
    def default_command(self) -> str:
        return ''


class Sink(Node):
    @property
    def default_command(self):
        return f"pactl set-default-sink {self.name}"


class Source(Node):
    @property
    def default_command(self):
        return f"pactl set-default-source {self.name}"


def parse_all_sinks() -> list[Sink]:
    return list(map(Sink, get_sink_strings()))


def parse_all_sources() -> list[Source]:
    return list(map(Source, get_source_strings()))
