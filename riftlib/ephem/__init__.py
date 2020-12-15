"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This subpackage implements a simple Ephemeris using
    the Python port of the Swiss Ephemeris (Pyswisseph).

    The pyswisseph library must be already installed and
    accessible.

"""

import riftlib
from . import swe


# Set default swefile path
swe.setPath(riftlib.PATH_RES + 'swefiles')

# Configure swefile path
def setPath(path):
    swe.setPath(path)