#!/usr/bin/env python3
import sys
from jeff.parser import getParser
from jeff.utils import checkDocker, loadConfig, loadPlugins, listContainers, \
    removeContainer

def main():
    if not checkDocker():
        return False

    config = loadConfig()
    if not config:
        return False

    parser, subparsers = getParser(config)
    commands = loadPlugins(config)

    for _, command in commands.items():
        command.parser(subparsers)

    args = parser.parse_args()

    if args.list:
        return listContainers(config)

    elif args.remove:
        return removeContainer(args.remove, config)

    elif args.command:
        return commands['jeff_%s' % args.command].run(args, config)

    else:
        parser.print_help()

def entryPoint():
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('')
