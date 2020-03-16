#!/usr/bin/env python3
class Style:
    """Shortcuts to terminal styling escape sequences"""

    BOLD = "\033[1m"
    END = "\033[0m"
    FG_Black = "\033[30m"
    FG_Red = "\033[31m"
    FG_Green = "\033[32m"
    FG_Yellow = "\033[33m"
    FG_Blue = "\033[34m"
    FG_Magenta = "\033[35m"
    FG_Cyan = "\033[36m"
    FG_White = "\033[37m"
    BG_Black = "\033[40m"
    BG_Red = "\033[41m"
    BG_Green = "\033[42m"
    BG_Yellow = "\033[43m"
    BG_Blue = "\033[44m"
    BG_Magenta = "\033[45m"
    BG_Cyan = "\033[46m"
    BG_White = "\033[47m"

    @staticmethod
    def bold(string):
        return f"{Style.BOLD}{string}{Style.END}"

    @staticmethod
    def red(string):
        return f"{Style.FG_Red}{string}{Style.END}"

    @staticmethod
    def green(string):
        return f"{Style.FG_Green}{string}{Style.END}"

    @staticmethod
    def blue(string):
        return f"{Style.FG_Blue}{string}{Style.END}"
