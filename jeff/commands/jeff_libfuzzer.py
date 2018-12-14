import subprocess
from jeff.utils import checkDir, checkImage, updateEnv, updateImage

def image():
    return {'name': 'jeffjerseycow/libfuzzer', 'version': 'v0.0.2'}

def parser(subparsers):
    fuzzParser = subparsers.add_parser('libfuzzer')
    fuzzParser.add_argument('directory', type=str, help='directory location to fuzz')
    fuzzParser.add_argument('-c', '--corpus', type=str, help='corpus directory')
    fuzzParser.add_argument('-a', '--artifacts', type=str, help='artifacts directory')
    fuzzParser.add_argument('--no-asan', action='store_true', help='disable address sanitizer')

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

    cmdArgs = ['docker', 'run', '--rm', '-ti', '-v', '%s:/in' % directory]

    corpus = checkDir(args.corpus)
    if corpus:
        cmdArgs = cmdArgs + ['-v', '%s:/corpus' % corpus]
    else:
        print('[-] corpus directory not set')

    artifacts = checkDir(args.artifacts)
    if artifacts:
        cmdArgs = cmdArgs + ['-v', '%s:/artifacts' % artifacts]
    else:
        print('[-] artifacts directory not set')

    cmdArgs = cmdArgs + updateEnv(compiler, flags, output)
    cmdArgs = cmdArgs + updateImage(imageDir, config)

    subprocess.run(cmdArgs)
    return True
