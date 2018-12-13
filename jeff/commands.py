import os
import subprocess
from jeff.utils import checkDir

def jeffDebug(args, flags, output, image):
    directory = checkDir(args.directory)
    if not directory:
        return False

    cmdArgs = ['docker', 'run', '--rm', '-ti', '--privileged', '-v', '%s:/in' % directory,
                '-e', 'FLAGS=%s' % ' '.join(flags), '-e', 'OUTPUT=%s' % ''.join(output),
                '%s:%s' % (image[0], image[1])]

    subprocess.run(cmdArgs)
    return True

def jeffFuzz(args, flags, output, image):
    directory = checkDir(args.directory)
    if not directory:
        return False

    cmdArgs = ['docker', 'run', '--rm', '-ti', '--privileged', '-v',
                '%s:/in' % directory, '-e', 'FLAGS=%s' % ' '.join(flags),
                '-e', 'OUTPUT=%s' % ''.join(output)]

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

    cmdArgs = cmdArgs + ['%s:%s' % (image[0], image[1])]

    subprocess.run(cmdArgs)
    return True
