import subprocess
from jeff.utils import checkDir, checkImage, updateEnv, updateImage

def image():
    return {'name': 'jeffjerseycow/debug', 'version': 'v0.0.1'}

def parser(subparsers):
    debugParser = subparsers.add_parser('debug')
    debugParser.add_argument('directory', type=str, help='directory location to debug')
    debugParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')

def getCFO(args, config):
    compiler = ['clang++']
    flags = ['-g', '-O0', '-fsanitize=fuzzer']

    if not args.no_asan:
        flags = flags + ['-fsanitize=address']

    output = ['fuzz.me']

    return compiler, flags, output

def run(args, config):
    imageDir = image()
    if not checkImage(imageDir, config):
        return False

    directory = checkDir(args.directory)
    if not directory:
        return False

    compiler, flags, output = getCFO(args, config)

    cmdArgs = ['docker', 'run', '--rm', '-ti', '--privileged', '-v', '%s:/in' % directory]
    cmdArgs = cmdArgs + updateEnv(compiler, flags, output)
    cmdArgs = cmdArgs + updateImage(imageDir, config)

    subprocess.run(cmdArgs)
    return True
