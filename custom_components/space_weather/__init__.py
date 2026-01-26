"""The NOAA Space Weather integration."""
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the NOAA Space Weather component."""
    _LOGGER.debug("NOAA Space Weather integration loaded")
    return True
