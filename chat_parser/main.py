"""Chat Parse.

Usage:
  chatparse [-v | --verbose]
  chatparse (-h | --help)
  chatparse --version

Options:
  -v --verbose  Show DEBUG logs.
  -h --help     Show this screen.
  --version     Show version.

Examples:
  cat examples/all.txt | chatparse
  cat examples/* | chatparse
  echo "@bob, come here real quick" | chatparse
"""
import logging
import sys

from docopt import docopt

from chat_parser import parse


def setup_logging(verbose=False):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    level = logging.DEBUG if verbose else logging.WARNING
    logger.setLevel(level)


def main():
    args = docopt(__doc__, version='Chat Parse 0.0.1')
    setup_logging(args['--verbose'])

    lines = ''.join(sys.stdin.readlines())

    print parse(lines)
