from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/afl', 'version': 'latest'}

def parser(subparsers):
    aflParser = subparsers.add_parser('afl')
    aflParser.add_argument('-d', '--directory', type=str, help='directory location to fuzz')
    aflParser.add_argument('-n', '--name', type=str, required=True, help='name of container')
    aflParser.add_argument('--no-update', action='store_true', help='do not update image')

def run(args, config):
    afl = JeffContainer(image(), args, config, privileged=True)

    if args.directory and not afl.addVolume(args.directory, '/afl'):
        return False

    afl.start()

    return True
