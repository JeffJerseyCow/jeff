#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from jeff.utils import loadConfig, loadCommands

def addSubparsers(subparsers):
    fuzzParser = subparsers.add_parser('libfuzzer')
    fuzzParser.add_argument('directory', type=str, help='directory location to fuzz')
    fuzzParser.add_argument('-c', '--corpus', type=str, help='corpus directory')
    fuzzParser.add_argument('-a', '--artifacts', type=str, help='artifacts directory')
    fuzzParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')

def main():
    # load configuration
    jeffConfig = loadConfig()
    if not jeffConfig:
        return False

    # create parsers
    parser = argparse.ArgumentParser('jeff')
    subparsers = parser.add_subparsers(dest='command')

    # load commands plugins
    commands = loadCommands(jeffConfig)

    # register parsers
    for _, module in commands.items():
        module.parser(subparsers)

    # parse arguments
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return False

    return True
    # check Docker installed
    if not checkDocker():
        return False

    # check images
    if not checkImages(IMAGES):
        return False

    # get arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    addSubparsers(subparsers)
    args = parser.parse_args()

    # check command has been set
    if not args.command :
        parser.print_help()
        return False

    # remove asan
    if args.no_asan:
        FLAGS.remove('-fsanitize=address')

    # select command
    if args.command == 'debug':
        return jeffDebug(args, FLAGS, OUTPUT, IMAGES[args.command])
    elif args.command == 'libfuzzer':
        return jeffFuzz(args, FLAGS, OUTPUT, IMAGES[args.command])

if __name__ == '__main__':
    sys.exit(main())
