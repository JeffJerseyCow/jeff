from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/ikos', 'version': 'latest'}

def parser(subparsers):
    ikosParser = subparsers.add_parser('ikos')
    ikosParser.add_argument('-d', '--directory', type=str, help='directory location to analyze')
    ikosParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    ikos = JeffContainer(image(), args, config)

    if ikos.checkContainer():
        return True

    if not ikos.checkImage():
        return False

    if args.directory and not ikos.addVolume(args.directory, '/ikos'):
        return False

    ikos.start()

    return True
