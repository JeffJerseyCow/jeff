#!/usr/bin/env python3
import sys
import argparse
from jeff.utils import loadConfig, loadCommands, checkDocker

def main():
    # check Docker installed
    if not checkDocker():
        return False

    # load configuration
    jeffConfig = loadConfig()
    if not jeffConfig:
        return False

    # create parsers
    parser = argparse.ArgumentParser('jeff')
    parser.add_argument('--version', action='version', version=jeffConfig['version'])
    subparsers = parser.add_subparsers(dest='command')

    # load commands plugins
    commands = loadCommands(jeffConfig)

    # register parsers
    for _, command in commands.items():
        command.parser(subparsers)

    # parse arguments
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return False

    # run command
    return commands['jeff_%s' % args.command].run(args, jeffConfig)

if __name__ == '__main__':
    sys.exit(main())
