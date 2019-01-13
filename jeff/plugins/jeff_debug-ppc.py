from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/debug-ppc', 'version': 'latest'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug-ppc')
    debugParser.add_argument('-d', '--directory', type=str, help='directory location to debug')
    debugParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    debugPpc = JeffContainer(image(), args, config, privileged=True)

    # check if container exists and load
    if debugPpc.checkContainer():
        return True

    # download image
    if not debugPpc.checkImage():
        return False

    if args.directory and not debugPpc.addVolume(args.directory, '/debug'):
        return False

    debugPpc.start()

    return True
