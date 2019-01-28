from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/debug-ppc', 'version': 'latest'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug-ppc')
    debugParser.add_argument('-d', '--directory', type=str, help='directory location to debug')
    debugParser.add_argument('-n', '--name', type=str, required=True, help='name of container')
    debugParser.add_argument('--no-update', action='store_true', help='do not update image')

def run(args, config):
    debugPpc = JeffContainer(image(), args, config, privileged=True)

    if args.directory and not debugPpc.addVolume(args.directory, '/debug'):
        return False

    debugPpc.start()

    return True
