import rofi_menu

import pactl


class AudioMenu(rofi_menu.Menu):
    """A menu to display the available sinks, selecting one of which will set it as default."""
    prompt = "Select default sink:"

    def __init__(self, **kwargs):
        """Creates a list of available sinks."""
        super().__init__(**kwargs)

        self.items = [rofi_menu.Item(sink['name']) for sink in pactl.parse_all_sinks()]
