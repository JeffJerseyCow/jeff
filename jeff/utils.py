import re
import os
import subprocess

def checkDocker():
    try:
        args = ['docker', 'version']
        subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=True)
        return True
    except FileNotFoundError:
        print('[-] install docker.io or docker ce')
    except subprocess.CalledProcessError:
        print('[-] add user "%s" to docker group' % os.getenv("USER"))
    return False

def checkImages(images):
    args = ['docker', 'image', 'ls']
    output = subprocess.run(args, check=True, stdout=subprocess.PIPE).stdout.decode()
    for k, v in images.items():
        r = re.compile(r'%s\s+%s' % (v[0], v[1]))
        if not r.search(output):
            args = ['docker', 'pull', '%s:%s' % (v[0], v[1])]
            try:
                subprocess.run(args, stderr=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError:
                print('[-] cannot download image %s:%s' % (v[0], v[1]))
                return False
    return True

def checkDir(dirPath):
    if not dirPath:
        return False

    if not os.path.isdir(dirPath):
        print('[-] directory "%s" doesn\'t exist' % dirPath)
        return False

    return os.path.realpath(dirPath)
