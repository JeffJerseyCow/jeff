from jeff.core import JeffContainer

def image():
    return {'name': 'jeffjerseycow/qsym', 'version': 'latest'}

def parser(subparsers):
    qsymParser = subparsers.add_parser('qsym')
    qsymParser.add_argument('-d', '--directory', type=str, help='directory location to analyse')
    qsymParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    qsym = JeffContainer(image(), args, config, privileged=True)

    if qsym.checkContainer():
        return True

    if not qsym.checkImage():
        return False

    if args.directory and not qsym.addVolume(args.directory, '/qsym'):
        return False

    qsym.addFlags(['--cap-add=SYS_PTRACE'])
    qsym.start()
    return True
