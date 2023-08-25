import re
import subprocess


def list_sinks() -> str:
    return subprocess.run(['pactl', 'list', 'sinks'], capture_output=True).stdout.decode()


def split_sinks(all_sinks: str) -> list[str]:
    return re.split(r'Sink #\d+', all_sinks)[1:]


def regex_match_one(pattern: str | re.Pattern[str], string: str) -> str:
    result = re.search(pattern, string, re.I)
    if result and len(result.groups()) == 1:
        return result.groups()[0]


def get_sink_attribute(sink: str, attr: str) -> str | None:
    return regex_match_one(rf'\n\s+{attr}: ([^\n]+)', sink)


def get_sink_property(sink: str, prop: str) -> str | None:
    return regex_match_one(rf'\n\s+{prop} = "([^\n]+)"\n', sink)


def parse_sink(sink: str) -> dict[str, str | None]:
    return {attr: get_sink_attribute(sink, attr) for attr in ['name', 'description']}


def parse_all_sinks() -> list[dict[str, str | None]]:
    return list(map(parse_sink, split_sinks(list_sinks())))
