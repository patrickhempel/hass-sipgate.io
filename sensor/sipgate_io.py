"""
Sensor for monitoring incoming and outgoing call with sipgate.io
"""

import asyncio
import logging

from homeassistant.core import callback
from homeassistant.components import http
from homeassistant.helpers.entity import Entity

API_ENDPOINT = '/api/sipgateio'

_LOGGER = logging.getLogger(__name__)


class SipgateIoSensor(Entity):
    """Representation of sipgate.io sensor"""

    def __init__(self):
        """Initialize the sensor"""
        self._name = "Hello!"
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor"""
        return 'sipgate.io call monitor'
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


    def set_device_state_attributes(self, attributes):
        self._attributes = attributes

    def set_state(self, state):
      self._state = state

    def update(self):
        """Update the new state data for the sensor,"""


class SipgateIoView(http.HomeAssistantView):
    """Handle Sipgate.io requests."""

    url = API_ENDPOINT
    name = 'api:sipgateio'

    def __init__(self, sensor):
      self._sensor = sensor

    @asyncio.coroutine
    def post(self, request):
        """Handle sipgate.io"""
        query = request.query

        _LOGGER.debug('Recieved sipgate.io request: %s', query['event'])

        attributes = {
            'from': query['from'],
            'to': query['to'],
            'event': query['event']
        }

        self._sensor.set_device_state_attributes(attributes)

        self._sensor.set_state(attributes['from'])


@asyncio.coroutine
def async_setup_platform(hass, config, add_devices, discovery_info=None):
  """Activate sipgate.io component."""

  sensor = SipgateIoSensor()
  view = SipgateIoView(sensor)

  hass.http.register_view(view)
  add_devices([sensor])
