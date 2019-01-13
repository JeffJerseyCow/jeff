from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/debug', 'version': 'latest'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('-d', '--directory', type=str, help='directory location to debug')
    debugParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    debug = JeffContainer(image(), args, config, privileged=True)

    if debug.checkContainer():
        return True

    if not debug.checkImage():
        return False

    if args.directory and not debug.addVolume(args.directory, '/debug'):
        return False

    debug.start()

    return True
