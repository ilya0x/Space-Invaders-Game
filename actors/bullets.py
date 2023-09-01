import math
import random

import pygame
from pygame import mixer

# CUSTOM LOOK FOR ERRORS DISPLAY
import pretty_errors

pretty_errors.configure(
    separator_character='*',
    line_color=pretty_errors.BRIGHT_RED + '-> ' + pretty_errors.default_config.line_color,
    lines_before=5,
    lines_after=5,
    code_color=pretty_errors.BLUE,
    filename_color=pretty_errors.BRIGHT_BLACK,
    function_color=pretty_errors.BLACK,
    line_number_color=pretty_errors.BRIGHT_GREEN + 'Line: '
)

class Bullets():
    ...

