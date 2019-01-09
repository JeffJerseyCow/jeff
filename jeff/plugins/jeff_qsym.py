import os
from jeff.core import checkDir, checkImage, checkContainer, updateEnv, updateImage, \
    updateVolume, startContainer, removeContainer

def imageDict():
    return {'name': 'jeffjerseycow/qsym', 'version': 'latest'}

def parser(subparsers):
    qsymParser = subparsers.add_parser('qsym')
    qsymParser.add_argument('-d', '--directory', type=str, help='directory location to fuzz')
    qsymParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

def run(args, config):
    # check if container exists and load
    if checkContainer(args, config):
        return True

    # download image
    image = imageDict()
    if not checkImage(image, config):
        return False

    # docker command string
    cmdArgs = ['docker', 'run', '-ti', '--privileged', '--name', args.name,
               '-h', args.name, '--cap-add=SYS_PTRACE']

    # finish command string
    if args.directory:
        cmdArgs = cmdArgs + updateVolume(args.directory, '/qsym')

    cmdArgs = cmdArgs + updateEnv('INITIALGID', os.getgid())
    cmdArgs = cmdArgs + updateEnv('INITIALUID', os.getuid())
    cmdArgs = cmdArgs + updateImage(image, config)
    startContainer(args.name, config, cmdArgs)

    return True
