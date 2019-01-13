import argparse

def getParser(config):
    """Create default jeff parser.

    Args:
        config: jeff configuration dictionary loaded with utils.loadConfig.

    Returns:
        The default jeff argument parser.
    """
    parser = argparse.ArgumentParser('jeff')
    mxGroup = parser.add_mutually_exclusive_group()
    mxGroup.add_argument('-l', '--list', action='store_true', help='list container(s)')
    mxGroup.add_argument('-r', '--remove', type=str, help='remove container')
    mxGroup.add_argument('--version', action='version', version=config['version'])
    subparsers = parser.add_subparsers(dest='command')
    return parser, subparsers
