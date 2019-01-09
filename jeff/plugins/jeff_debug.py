import os
from jeff.core import checkDir, checkImage, checkContainer, updateEnv, updateImage, \
    updateVolume, startContainer, removeContainer

def imageDict():
    return {'name': 'jeffjerseycow/debug', 'version': 'latest'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('-d', '--directory', type=str, help='directory location to debug')
    debugParser.add_argument('-n', '--name', type=str, required=True, help='name of container')

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
               '-h', args.name]

    # finish command string
    if args.directory:
        cmdArgs = cmdArgs + updateVolume(args.directory, '/debug')

    cmdArgs = cmdArgs + updateEnv('INITIALGID', os.getgid())
    cmdArgs = cmdArgs + updateEnv('INITIALUID', os.getuid())
    cmdArgs = cmdArgs + updateImage(image, config)
    startContainer(args.name, config, cmdArgs)

    return True
