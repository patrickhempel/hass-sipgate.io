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

@asyncio.coroutine
def async_setup_platform(hass, config, add_devices, discovery_info=None):
    """Activate sipgate.io component."""
    hass.http.register_view(SipgateIoView)
    add_devices([SipgateIoSensor()])

class SipgateIoSensor(Entity):
    """Representation of sipgate.io sensor"""

    def __init__(self):
        """Initialize the sensor"""
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

    def update(self):
        """Update the new state data for the sensor,"""


class SipgateIoView(http.HomeAssistantView):
    """Handle Sipgate.io requests."""

    url = API_ENDPOINT
    name = 'api:sipgateio'

    @asyncio.coroutine
    def post(self, request):
        """Handle sipgate.io"""
        hass = request.app['hass']
        query = request.query
        
        _LOGGER.debug('Recieved sipgate.io request: %s', query)