import os
import subprocess
from jeff.core import checkDir, checkImage, checkContainer, updateEnv, updateImage, \
    updateVolume, removeContainer

def imageDict():
    return {'name': 'jeffjerseycow/debug', 'version': 'v0.0.2'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('-d', '--directory', type=str, help='directory location to debug')
    debugParser.add_argument('-n', '--name', type=str, required=True, help='name of container')
    debugParser.add_argument('--rm', action='store_true', help='delete container')

def run(args, config):
    # remove container
    if args.rm and removeContainer(args):
        return True
    elif args.rm:
        return False

    # check if container exists and load
    if checkContainer(args):
        return True

    # download image
    image = imageDict()
    if not checkImage(image, config):
        return False

    # docker command string
    cmdArgs = ['docker', 'run', '-ti', '--privileged', '--name', '%s' % args.name]

    # finish command string
    if args.directory:
        cmdArgs = cmdArgs + updateVolume(args.directory, '/debug')
    else:
        print('[-] directory not specified')

    cmdArgs = cmdArgs + updateEnv('INITIALGID', os.getgid())
    cmdArgs = cmdArgs + updateEnv('INITIALUID', os.getuid())
    cmdArgs = cmdArgs + updateImage(image, config)
    subprocess.run(cmdArgs)

    return True
