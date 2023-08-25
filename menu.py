import rofi_menu

import pactl


class AudioMenu(rofi_menu.Menu):
    """A menu to display the available sinks, selecting one of which will set it as default."""
    prompt: str
    items: list[rofi_menu.Item]

    def __init__(self, **kwargs):
        """Creates a list of available sinks."""
        super().__init__(**kwargs)

        self.prompt = "Select default sink:"

        self.items = []
        for sink in pactl.parse_all_sinks():
            kwargs = {'flags': [rofi_menu.FLAG_STYLE_URGENT]} if sink.current else {}
            self.items.append(
                rofi_menu.ShellItem(
                    sink.description,
                    sink.default_command,
                    **kwargs
                )
            )
