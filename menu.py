import rofi_menu

import pactl


class AudioMenu(rofi_menu.Menu):
    """A menu to display the available sinks, selecting one of which will set it as default."""
    prompt = "Select Default Sink:"

    def __init__(self, **kwargs):
        """Creates a list of available sinks."""
        super().__init__(**kwargs)

        self.items = [rofi_menu.Item(pactl.list_sinks())]
