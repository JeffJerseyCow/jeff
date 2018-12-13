#!/usr/bin/env python3
import sys
import argparse
import subprocess
from jeff.utils import checkDocker, checkImages
from jeff.commands import jeffDebug, jeffFuzz

IMAGES = {'llvm': ('jeffjerseycow/llvm', '8.0'),
          'libfuzzer': ('jeffjerseycow/libfuzzer', 'v0.0.2'),
          'debug': ('jeffjerseycow/debug', 'v0.0.1')}

FLAGS = ['-g', '-O0', '-fsanitize=fuzzer', '-fsanitize=address']

OUTPUT = ['fuzz.me']

def addSubparsers(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('directory', type=str, help='directory location to debug')
    debugParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')

    fuzzParser = subparsers.add_parser('libfuzzer')
    fuzzParser.add_argument('directory', type=str, help='directory location to fuzz')
    fuzzParser.add_argument('-c', '--corpus', type=str, help='corpus directory')
    fuzzParser.add_argument('-a', '--artifacts', type=str, help='artifacts directory')
    fuzzParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')

def main():
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
