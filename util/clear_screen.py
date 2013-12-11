# -*- coding: utf-8 -*-
"""
Helper module. It provides the clear_screen function, which clears the screen.
*duh!*
"""
__author__ = "1224270: Frank Kramer, 3402993: Sascha Reynolds"

import os


def clear_screen():
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('cls')
    else:
        print(80 * "\n")
