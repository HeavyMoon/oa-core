# sound.py - Play audio.

import logging
_logger = logging.getLogger(__name__)

import subprocess

from oa.modules.abilities.core import get, put

def _in(ctx):
    while not ctx.finished.is_set():
        path = get()
        
        # Pause listening while talking. Mute STT.
        put('speech_recognition','mute')

        try:
            subprocess.call(f'aplay {path}', shell=True)
        except Exception as ex:
            _logger.error("Error playing sound: {}".format(ex))

        # Audio complete. Begin listening. Unmute STT.
        put('speech_recognition','unmute')
