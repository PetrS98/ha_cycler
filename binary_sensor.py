import logging
import datetime

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

def setup_platform(hass, config, add_entities, discovery_info=None):
    Sensors = []

    TimeFrom = config.get(CONF_TIME_FROM)
    OnTime = config.get(CONF_ON_TIME)
    OffTime = config.get(CONF_OFF_TIME)

    add_entities(CyclerSensor(TimeFrom, OnTime, OffTime), update_before_add=True)

class CyclerSensor(BinarySensorEntity):
    _timeFrom = None
    _onTime = None
    _offTime = None

    _nextAction = None
    
    def __init__(self, TimeFrom, OnTime, OffTime):
        """Initialize the sensor."""
        
        self._init = True
        self._available = None
        self._active = None
        self._enableOpertation = True

        self._timeFrom = TimeFrom
        self._onTime = OnTime
        self._offTime = OffTime

        self.update()

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

            if self._init and (ActualTime.hour == self._timeFrom.hour and ActualTime.minute == self._timeFrom.minute):
                
                self._init = False
                self._active = True
                self._nextAction = (ActualTime + self._onTime)

            elif self._active and (ActualTime.hour == self._nextAction.hour and ActualTime.minute == self._nextAction.minute):
                if self._enableOpertation:
                    self._active = False
                    self._nextAction = (ActualTime + self._offTime)
                self._enableOpertation = False
                
            elif self._active == False and (ActualTime.hour == self._nextAction.hour and ActualTime.minute == self._nextAction.minute):
                if self._enableOpertation:
                    self._active = True
                    self._nextAction = (ActualTime + self._onTime)
                self._enableOpertation = False

            else:
                self._enableOpertation = True
            self._available = True
        except:
            _LOGGER.exception("Error occured in cycler logic")
            self._available = False
