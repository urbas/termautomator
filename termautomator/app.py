import argparse

import logging


def run():
    args = _parse_args()
    _setupLogging(args.verbose)


def _parse_args():
    parser = argparse.ArgumentParser(description="Edit Raspbian's /boot/cmdline.txt.")

    parser.add_argument("-v", "--verbose", action='count', default=0,
                        help="Verbosity level. Default: errors and warnings only.")

    return parser.parse_args()


def _setupLogging(verbosity_level):
    level = logging.WARN
    if verbosity_level == 1:
        level = logging.INFO
    elif verbosity_level >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='[%(levelname)s:%(name)s] %(asctime)s %(message)s')
