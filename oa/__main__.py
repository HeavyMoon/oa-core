# Open Assistant 0.21
# 2018 General Public License V3

"""Open Assistant reference implementation."""

import logging
_logger = logging.getLogger(__name__)

import os

import oa

import oa.legacy

def start(hub, **kwargs):
    """Initialize and run the OpenAssistant Agent"""
    from oa.util.repl import command_loop

    hub.run()

    _map = [
        ('ear', 'speech_recognition'),
        ('speech_recognition', 'mind'),
    ]
    for _in, _out in _map:
        hub.parts[_in].output += [hub.parts[_out]]

    while not hub.finished.is_set():
        try:
            command_loop(hub)
        except Exception as ex:
            _logger.error("Command Loop: {}".format(ex))

    hub.ready.wait()


if __name__ == '__main__':
    import sys

    from oa.util.args import _parser
    args = _parser(sys.argv[1:])

    log_template = "[%(asctime)s] %(levelname)s %(threadName)s %(name)s: %(message)s"
    logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG, filename=args.log_file, format=log_template)

    print('\033[1m')    # BOLD
    print('\033[32m')   # GREEN
    print('     ____                      ___              _      __              __   ')
    print('    / __ \___  ____  ____     /   |  __________(_)____/ /_____ _____  / /_  ')
    print('   / / / / _ \/ __ \/ __ \   / /| | / ___/ ___/ / ___/ __/ __ `/ __ \/ __/  ')
    print('  / /_/ /  __/ /_/ / / / /  / ___ |(__  |__  ) (__  ) /_/ /_/ / / / / /_    ')
    print('  \____/\___/ .___/_/ /_/  /_/  |_/____/____/_/____/\__/\__,_/_/ /_/\__/    ')
    print('           /_/                                                              ')
    print('\033[0m')    # RESET
    _logger.info("Start Open Assistant")

    config = {
        'module_path': [
            os.path.join(os.path.dirname(__file__), 'modules'),
        ],
        'modules': [
            'voice',
            'sound',
            'ear',
            'speech_recognition',
            'mind',
        ],
    }

    import json
    config_path = args.config_file
    if config_path is not None:
        config.update(json.load(open(config_path)))

    hub = oa.Hub(config=config)

    # XXX: temporary compatability hack
    oa.legacy.hub = hub
    oa.legacy.core_directory = os.path.dirname(__file__)

    try:
        start(
            hub,
            config_path=args.config_file,
        )

    except KeyboardInterrupt:
        _logger.info("Ctrl-C Pressed")

        _logger.info("Signaling Shutdown")
        hub.finished.set()

        _logger.info('Waiting on threads')
        [thr.join() for thr in hub.thread_pool]
        _logger.info('Threads closed')
