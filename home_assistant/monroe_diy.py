"""
Support for monroe DIY covers.

This custom component supports Monroe DIY curtains.
http://vignesh.foamsnet.com/2018/06/v20-ok-google-open-my-curtains.html
"""
import os
import requests
import voluptuous as vol

from homeassistant.components.cover import (CoverDevice, ATTR_POSITION, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_COVERS, CONF_FRIENDLY_NAME,
    STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING)
from homeassistant.util.json import load_json, save_json
import homeassistant.helpers.config_validation as cv

CONF_IP_ADDRESS = "ip_address"
CONF_FULL_OPEN_COUNT = "full_open_count"
CONF_OPEN_DIRECTION = "open_direction"
CONF_CLOSE_DIRECTION = "close_direction"
CONF_STOP_COMMAND = "stop_command"

FULLY_CLOSED = 0
FULLY_OPEN = 100
ONE_ROTATION = 800

COVER_SCHEMA = vol.Schema({
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_FULL_OPEN_COUNT): cv.positive_int,
    vol.Optional(CONF_OPEN_DIRECTION, default="right"): cv.string,
    vol.Optional(CONF_CLOSE_DIRECTION, default="left"): cv.string,
    vol.Optional(CONF_STOP_COMMAND, default="off"): cv.string,
    vol.Optional(CONF_FRIENDLY_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_COVERS): vol.Schema({cv.slug: COVER_SCHEMA}),
})

STATE_JSON_FILE = ".monroe_diy_state.json"

def setup_platform(hass, config, add_devices, discovery_info=None):
    devices = config.get(CONF_COVERS, {})
    covers = []
    for device_name, device_config in devices.items():
        covers.append(MonroeDiyCover(hass, device_name, device_config))
    if covers:
        add_devices(covers, True)

class MonroeDiyCover(CoverDevice):
    """Representation of a Monroe DIY cover."""

    def __init__(self, hass, name, config):
        self._name = name
        self._ip_address = config.get(CONF_IP_ADDRESS)
        self._full_open_count = config.get(CONF_FULL_OPEN_COUNT)
        self._open_direction = config.get(CONF_OPEN_DIRECTION)
        self._close_direction = config.get(CONF_CLOSE_DIRECTION)
        self._stop_command = config.get(CONF_STOP_COMMAND)
        self._friendly_name = config.get(CONF_FRIENDLY_NAME, name)
        self._locked = False
        self._is_opening = False
        self._is_closing = False
        self._hass = hass
        self._state = self._load_json().get(name, 0)

    def _load_json(self):
        state_json_path = self._hass.config.path(STATE_JSON_FILE)
        if os.path.isfile(state_json_path):
            state_json = load_json(state_json_path)
            return state_json
        else:
            return {}

    def _save_position(self, position):
        state_json = self._load_json()
        state_json[self._name] = position
        state_json_path = self._hass.config.path(STATE_JSON_FILE)
        save_json(state_json_path, state_json)

    def _set_position(self, position):
        if self._locked:
            return
        delta_position = position - self._state
        if not delta_position:
            return
        self._locked = True
        command = self._open_direction if delta_position > 0 else self._close_direction
        if (delta_position > 0):
            self._is_opening = True
        else:
            self._is_closing = True
        delta_position = abs(delta_position)
        rotations = int(ONE_ROTATION * self._full_open_count * (delta_position / 100.0))
        url = "http://%s/%s/%d" % (self._ip_address, command, rotations)
        try:
            requests.get(url, timeout = 60)
        except:
            pass
        self._state = position
        self._save_position(position)
        self._locked = False
        self._is_opening = False
        self._is_closing = False

    @property
    def name(self):
        return self._friendly_name

    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def is_closed(self):
        return self._state == FULLY_CLOSED

    @property
    def state(self):
        if self._is_opening:
            return STATE_OPENING
        if self._is_closing:
            return STATE_CLOSING
        return STATE_CLOSED if self._state == FULLY_CLOSED else STATE_OPEN

    @property
    def current_cover_position(self):
        return self._state

    def open_cover(self, **kwargs):
        self._set_position(FULLY_OPEN)

    def close_cover(self, **kwargs):
        self._set_position(FULLY_CLOSED)

    def set_cover_position(self, **kwargs):
        position = kwargs.get(ATTR_POSITION)
        self._set_position(position)