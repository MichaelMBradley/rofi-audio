import abc
import re
import subprocess
import enum


class NodeType(enum.StrEnum):
    sink = 'sink'
    source = 'source'


def run_pactl_command(args: list[str]) -> str:
    return subprocess.run(['pactl', *args], capture_output=True).stdout.decode()


def list_nodes_string(node: NodeType) -> str:
    return run_pactl_command(['list', f"{node.value}s"])


def get_default_node(node: NodeType) -> str:
    return run_pactl_command([f'get-default-{node.value}'])


def get_sink_strings() -> list[str]:
    return re.split(r'Sink #\d+', list_nodes_string(NodeType.sink))[1:]


def get_source_strings() -> list[str]:
    return re.split(r'Source #\d+', list_nodes_string(NodeType.source))[1:]


def regex_match_one(pattern: str | re.Pattern[str], string: str) -> str:
    result = re.search(pattern, string, re.I)
    if result and len(result.groups()) == 1:
        return result.groups()[0]


def get_attribute(sink: str, attr: str) -> str | None:
    return regex_match_one(rf'\n\s+{attr}: ([^\n]+)', sink)


def get_property(sink: str, prop: str) -> str | None:
    return regex_match_one(rf'\n\s+{prop} = "([^\n]+)"\n', sink)


CURRENT_SINK = get_default_node(NodeType.sink).strip()
CURRENT_SOURCE = get_default_node(NodeType.source).strip()


class Node(abc.ABC):
    current: bool

    def __init__(self, sink_data: str):
        self.name = get_attribute(sink_data, 'Name')
        self.description = get_attribute(sink_data, 'Description')
        self.mute = get_attribute(sink_data, 'Mute') != 'no'
        self.current = False

    def __str__(self) -> str:
        return self.description or self.name or "No sink data available"

    @property
    def default_command(self) -> str:
        return ''


class Sink(Node):
    def __init__(self, sink_data: str):
        super().__init__(sink_data)
        self.current = self.name == CURRENT_SINK

    @property
    def default_command(self):
        return f"pactl set-default-sink {self.name}"


class Source(Node):
    def __init__(self, sink_data: str):
        super().__init__(sink_data)
        self.current = self.name == CURRENT_SOURCE

    @property
    def default_command(self):
        return f"pactl set-default-source {self.name}"


def parse_all_sinks() -> list[Sink]:
    return list(map(Sink, get_sink_strings()))


def parse_all_sources() -> list[Source]:
    return list(map(Source, get_source_strings()))
