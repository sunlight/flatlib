"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)


    This module implements a class to represent an
    astrology Chart. It provides methods to handle
    the chart, as well as three relevant properties:

    - objects: a list with the chart's objects
    - houses: a list with the chart's houses
    - angles: a list with the chart's angles

    Since houses 1 and 10 may not match the Asc and
    MC in some house systems, the Chart class
    includes the list of angles. The angles should be
    used when you want to deal with angle's longitudes.

    There are also methods to access fixed stars.

"""

from . import angle
from . import const
from . import utils
from .ephem import ephem
from .datetime import Datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta


# ------------------ #
#    Chart Class     #
# ------------------ #

class Chart:
    """ This class represents an astrology chart. """

    def __init__(self, date, pos, **kwargs):
        """ Creates an astrology chart for a given
        date and location.

        Optional arguments are:
        - hsys: house system
        - IDs: list of objects to include

        """
        # Handle optional arguments
        hsys = kwargs.get('hsys', const.HOUSES_DEFAULT)
        IDs = kwargs.get('IDs', const.LIST_OBJECTS_TRADITIONAL)

        self.date = date
        self.pos = pos
        self.hsys = hsys
        self.objects = ephem.getObjectList(IDs, date, pos)
        self.houses, self.angles = ephem.getHouses(date, pos, hsys)

    def copy(self):
        """ Returns a deep copy of this chart. """
        chart = Chart.__new__(Chart)
        chart.date = self.date
        chart.pos = self.pos
        chart.hsys = self.hsys
        chart.objects = self.objects.copy()
        chart.houses = self.houses.copy()
        chart.angles = self.angles.copy()
        return chart


    # === Properties === #

    def getObject(self, ID):
        """ Returns an object from the chart. """
        return self.objects.get(ID)

    def getHouse(self, ID):
        """ Returns an house from the chart. """
        return self.houses.get(ID)

    def getAngle(self, ID):
        """ Returns an angle from the chart. """
        return self.angles.get(ID)

    def get(self, ID):
        """ Returns an object, house or angle
        from the chart.

        """
        if ID.startswith('House'):
            return self.getHouse(ID)
        elif ID in const.LIST_ANGLES:
            return self.getAngle(ID)
        else:
            return self.getObject(ID)


    # === Fixed stars === #

    # The computation of fixed stars is inefficient,
    # so the access must be made directly to the
    # ephemeris only when needed.

    def getFixedStar(self, ID):
        """ Returns a fixed star from the ephemeris. """
        return ephem.getFixedStar(ID, self.date)

    def getFixedStars(self):
        """ Returns a list with all fixed stars. """
        IDs = const.LIST_FIXED_STARS
        return ephem.getFixedStarList(IDs, self.date)


    # === Houses and angles === #

    def isHouse1Asc(self):
        """ Returns true if House1 is the same as the Asc. """
        house1 = self.getHouse(const.HOUSE1)
        asc = self.getAngle(const.ASC)
        dist = angle.closestdistance(house1.lon, asc.lon)
        return abs(dist) < 0.0003  # 1 arc-second

    def isHouse10MC(self):
        """ Returns true if House10 is the same as the MC. """
        house10 = self.getHouse(const.HOUSE10)
        mc = self.getAngle(const.MC)
        dist = angle.closestdistance(house10.lon, mc.lon)
        return abs(dist) < 0.0003  # 1 arc-second


    # === Other properties === #

    def isDiurnal(self):
        """ Returns true if this chart is diurnal. """
        sun = self.getObject(const.SUN)
        mc = self.getAngle(const.MC)

        # Get ecliptical positions and check if the
        # sun is above the horizon.
        lat = self.pos.lat
        sunRA, sunDecl = utils.eqCoords(sun.lon, sun.lat)
        mcRA, mcDecl = utils.eqCoords(mc.lon, 0)
        return utils.isAboveHorizon(sunRA, sunDecl, mcRA, lat)

    def getMoonPhase(self):
        """ Returns the phase of the moon. """
        sun = self.getObject(const.SUN)
        moon = self.getObject(const.MOON)
        dist = angle.distance(sun.lon, moon.lon)
        if dist < 90:
            return const.MOON_FIRST_QUARTER
        elif dist < 180:
            return const.MOON_SECOND_QUARTER
        elif dist < 270:
            return const.MOON_THIRD_QUARTER
        else:
            return const.MOON_LAST_QUARTER


    # === Solar returns === #

    def solarReturn(self, year, pos=0):
        """ Returns this chart's solar return for a
        given year.

        """
        if pos == 0:
            pos = self.pos

        sun = self.getObject(const.SUN)
        date = Datetime(date='{0}-01-01'.format(year), time='00:00', pos=pos)
        srDate = ephem.nextSolarReturn(date, sun.lon)
        return Chart(srDate, pos, hsys=self.hsys)


    # === Progressions === #

    def progressedChart(self, date, pos=0):
        """ Return the progressed chart for a
        given date.

        """
        if pos == 0:
            pos = self.pos

        day_length = 23.9344    # 23 hours 56 minutes 4 seconds
        tz = self.date.getTz(pos)
        progression_date = tz.localize(datetime.fromisoformat(date))
        chart_date = self.date.datetime
        start_date = tz.localize(chart_date)
        last_date = start_date.replace(year=progression_date.year)

        # the progression year is counted from birthday to birthday
        # this calculates how far along in the year the progression date is
        if last_date > progression_date:
            next_date = last_date
            last_date -= relativedelta(years=1)
        else:
            next_date = last_date + relativedelta(years=1)

        year_length = (next_date - last_date).days * day_length
        days_passed = (progression_date - last_date).days * day_length
        days_passed += relativedelta(progression_date, last_date).hours
        days_passed_ratio = days_passed / year_length

        # calculate progression chart date / time
        days = relativedelta(progression_date, start_date).years
        hours = days_passed_ratio * day_length
        pcd = chart_date + relativedelta(days=days, hours=hours)
        progressed_chart_date = Datetime(date=[pcd.year, pcd.month, pcd.day], time=['+', pcd.hour, pcd.minute, pcd.second], pos=pos)
        return Chart(progressed_chart_date, pos, hsys=self.hsys)


    # === Transits === #

    def transits(self, date=0, pos=0):
        """ Returns another chart based on new date.

        """
        if date == 0:
            now = datetime.now()
            transit_date = now.strftime("%Y-%m-%d")
            transit_time = now.strftime("%H:%M:%S")
            date = Datetime(date=transit_date, time=transit_time, pos=pos)

        if pos == 0:
            pos = self.pos

        return Chart(date, pos, hsys=self.hsys)
