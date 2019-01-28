from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/qsym', 'version': 'latest'}

def parser(subparsers):
    qsymParser = subparsers.add_parser('qsym')
    qsymParser.add_argument('-d', '--directory', type=str, help='directory location to analyse')
    qsymParser.add_argument('-n', '--name', type=str, required=True, help='name of container')
    qsymParser.add_argument('--no-update', action='store_true', help='do not update image')

def run(args, config):
    qsym = JeffContainer(image(), args, config, privileged=True)

    if args.directory and not qsym.addVolume(args.directory, '/qsym'):
        return False

    qsym.addFlags(['--cap-add=SYS_PTRACE'])
    qsym.start()
    return True
