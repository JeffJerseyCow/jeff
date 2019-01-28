from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/libfuzzer', 'version': 'latest'}

def parser(subparsers):
    libfuzzerParser = subparsers.add_parser('libfuzzer')
    libfuzzerParser.add_argument('-d', '--directory', type=str, help='directory location to fuzz')
    libfuzzerParser.add_argument('-n', '--name', type=str, required=True, help='name of container')
    libfuzzerParser.add_argument('--no-update', action='store_true', help='do not update image')

def run(args, config):
    libfuzzer = JeffContainer(image(), args, config)

    if args.directory and not libfuzzer.addVolume(args.directory, '/libfuzzer'):
        return False

    libfuzzer.start()

    return True
