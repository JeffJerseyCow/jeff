from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/libfuzzer', 'version': 'latest'}

def parser(subparsers):
    libfuzzerParser = subparsers.add_parser('libfuzzer')
    libfuzzerParser.add_argument('-d', '--directory', type=str, help='directory location to fuzz')
    libfuzzerParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    libfuzzer = JeffContainer(image(), args, config)

    # check if container exists and load
    if libfuzzer.checkContainer():
        return True

    # download image
    if not libfuzzer.checkImage():
        return False

    if args.directory and not libfuzzer.addVolume(args.directory, '/libfuzzer'):
        return False

    libfuzzer.start()

    return True
