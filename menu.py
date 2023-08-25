import pathlib

import rofi_menu

import pactl


CURRENT_ICON = pathlib.Path(__file__).parent / 'assets/current.svg'


class AudioMenu(rofi_menu.Menu):
    """A menu to display the available sinks, selecting one of which will set it as default."""
    prompt: str
    items: list[rofi_menu.Item]

    def __init__(self, **kwargs):
        """Creates a list of available sinks."""
        super().__init__(**kwargs)

        self.prompt = "Select default sink/source:"

        self.items = [rofi_menu.Item("--- Sinks ---", nonselectable=True)]
        for sink in pactl.parse_all_sinks():
            item_kwargs = {}
            if sink.current:
                item_kwargs['flags'] = [rofi_menu.FLAG_STYLE_URGENT]
                item_kwargs['icon'] = CURRENT_ICON
            self.items.append(
                rofi_menu.ShellItem(
                    f"  {sink.description}",
                    sink.default_command,
                    show_output=True,
                    **item_kwargs
                )
            )

        self.items.append(rofi_menu.Item("-- Sources --", nonselectable=True))
        for source in pactl.parse_all_sources():
            item_kwargs = {}
            if source.current:
                item_kwargs['flags'] = [rofi_menu.FLAG_STYLE_URGENT]
                item_kwargs['icon'] = CURRENT_ICON
            self.items.append(
                rofi_menu.ShellItem(
                    f"  {source.description}",
                    source.default_command,
                    **item_kwargs
                )
            )
