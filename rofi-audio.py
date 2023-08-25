#!/home/mbradley/dev/rofi-audio/venv/bin/python
import rofi_menu

import menu


if __name__ == "__main__":
    rofi_menu.run(menu.AudioMenu(), rofi_version="1.6")
