import logging
import datetime
import math

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import BinarySensorEntity


""" Constants """
DEVICE_CLASS = "monetary"
COURSE_CODE = "EUR"

CONF_TIME_FROM = "time_from"
CONF_ON_TIME = "on_time"
CONF_OFF_TIME = "off_time"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TIME_FROM): cv.time,
        vol.Required(CONF_ON_TIME): cv.time,
        vol.Required(CONF_OFF_TIME): cv.time
    }
)

_LOGGER = logging.getLogger(__name__)

def TimeAddition(t1, t2):
    nextTimeMs = TimeToMs(t1) + TimeToMs(t2)

    if CheckTimeOverflow(nextTimeMs):
        dif = nextTimeMs - 86400000
        timeList = MsToTime(dif)
        return datetime.time(timeList[0], timeList[1], timeList[2], timeList[3])
    else:
        timeList = MsToTime(nextTimeMs)
        return datetime.time(timeList[0], timeList[1], timeList[2], timeList[3])

def TimeToMs(t):
    tmp = (t.hour * 3600000)
    tmp = tmp + (t.minute * 60000)
    tmp = tmp + (t.second * 1000)
    tmp = tmp + (int(t.microsecond))
    return tmp

def MsToTime(timeMs):
    listTime = []
    listTime.append(math.floor(timeMs / 3600000))
    tmp = (timeMs % 3600000)
    listTime.append(math.floor(tmp / 60000))
    tmp = (tmp % 60000)
    listTime.append(math.floor(tmp / 1000))
    listTime.append((tmp % 1000))

    return listTime

def CheckTimeOverflow(TimeInMs):
    return TimeInMs >= 86400000

def setup_platform(hass, config, add_entities, discovery_info=None):
    
    TimeFrom = config.get(CONF_TIME_FROM)
    OnTime = config.get(CONF_ON_TIME)
    OffTime = config.get(CONF_OFF_TIME)

    add_entities([CyclerSensor(TimeFrom, OnTime, OffTime)], update_before_add=True)

class CyclerSensor(BinarySensorEntity):
    _timeFrom = None
    _onTime = None
    _offTime = None

    _nextAction = datetime.time(0,0,0)
    
    def __init__(self, TimeFrom, OnTime, OffTime):
        """Initialize the sensor."""
        
        self._available = None
        self._active = False

        self._timeFrom = TimeFrom
        self._onTime = OnTime
        self._offTime = OffTime

        self._nextAction = TimeFrom

    @property
    def name(self):
        return "Cycler"

    @property
    def is_on(self):
        return self._active

    @property
    def available(self):
        return self._available

    @property
    def unique_id(self):
        return "Home Assistant Cycler by PS"

    def update(self):
        try:
            ActualTime = datetime.datetime.now().time()

            if ActualTime.hour >= self._nextAction.hour and ActualTime.minute > self._nextAction.minute:

                self._nextAction = TimeAddition(self._nextAction, self._onTime)
                self._nextAction = TimeAddition(self._nextAction, self._offTime)

            elif self._active and (ActualTime.hour == self._nextAction.hour and ActualTime.minute == self._nextAction.minute):
                
                self._active = False
                self._nextAction = TimeAddition(self._nextAction, self._offTime)
                
            elif self._active == False and (ActualTime.hour == self._nextAction.hour and ActualTime.minute == self._nextAction.minute):
                
                self._active = True
                self._nextAction = TimeAddition(self._nextAction, self._onTime)
            self._available = True
        except:
            _LOGGER.exception("Error occured in cycler logic")
            self._available = False