# -*- coding: utf-8 -*-
"""
This helper module provides to logic to decide how key presses are caught and
handled.
"""
__author__ = "1224270: Frank Kramer, 3402993: Sascha Reynolds"

import os

try:
    if os.name in ("nt", "dos", "ce"):
        from msvcrt import getch
    else:
        def getch():
            os.system("bash -c \"read -n 1\"")
except:
    getch = input()
