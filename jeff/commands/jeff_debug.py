import subprocess
from jeff.utils import checkDir

def run(args, config, image):
    directory = checkDir(args.directory)
    if not directory:
        return False

    cmdArgs = ['docker', 'run', '--rm', '-ti', '--privileged', '-v', '%s:/in' % directory,
                '-e', 'FLAGS=%s' % ' '.join(flags), '-e', 'OUTPUT=%s' % ''.join(output),
                '%s:%s' % (image[0], image[1])]

    subprocess.run(cmdArgs)
    return True

def image():
    return {image: 'jeffjerseycow/debug',
            version: 'v0.0.1'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('directory', type=str, help='directory location to debug')
    debugParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')
