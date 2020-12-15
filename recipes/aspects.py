"""
    Author: João Ventura <flatangleweb@gmail.com>
    
    
    This recipe shows sample code for handling 
    aspects.

"""

from riftlib import aspects
from riftlib import const
from riftlib.chart import Chart
from riftlib.datetime import Datetime
from riftlib.geopos import GeoPos


# Build a chart for a date and location
date = Datetime('2015/03/13', '17:00', '+00:00')
pos = GeoPos('38n32', '8w54')
chart = Chart(date, pos)

# Retrieve the Sun and Moon 
sun = chart.get(const.SUN)
moon = chart.get(const.MOON)

# Get the aspect
aspect = aspects.getAspect(sun, moon, const.MAJOR_ASPECTS)
print(aspect)     # <Moon Sun 90 Applicative +00:24:30>