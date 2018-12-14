import re
import os
import json
import importlib
import subprocess

def loadConfig():
    jeffDirPath = os.path.dirname(__file__)
    jeffConfigPath = os.path.join(jeffDirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(jeffConfigPath):
        print('[-] missing configuration file')
        return False

    with open(jeffConfigPath, 'r') as configFile:
        return json.loads(configFile.read())

def loadCommands(config):
    commands = {}
    importPrefix = 'jeff.commands'

    for name in config['commands']:
        commands[name] = importlib.import_module('%s.%s' % (importPrefix, name))

    return commands

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

def checkImage(image, config):
    imageVersion = image['version']

    if config['baseDomain'] != '':
        imageName = '%s/%s' % (config['baseDomain'], image['name'])
    else:
        imageName = image['name']

    args = ['docker', 'image', 'ls']
    output = subprocess.run(args, check=True, stdout=subprocess.PIPE).stdout.decode()
    r = re.compile(r'%s\s+%s' % (imageName, imageVersion))

    if not r.search(output):
        args = ['docker', 'pull', '%s:%s' % (imageName, imageVersion)]

        try:
            subprocess.run(args, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            print('[-] cannot download image %s:%s' % (imageName, imageVersion))
            return False

    return True

def checkDir(dirPath):
    if not dirPath:
        return False

    if not os.path.isdir(dirPath):
        print('[-] directory "%s" doesn\'t exist' % dirPath)
        return False

    return os.path.realpath(dirPath)

def updateEnv(compiler, flags, output):
    cmdArgs = ['-e', 'COMPILER=%s' % ''.join(compiler),
               '-e', 'FLAGS=%s' % ' '.join(flags),
               '-e', 'OUTPUT=%s' % ''.join(output)]
    return cmdArgs

def updateImage(image, config):
    if config['baseDomain'] != '':
        return ['%s/%s:%s' % (config['baseDomain'], image['name'], image['version'])]
    else:
        return ['%s:%s' % (image['name'], image['version'])]

def updateConfig(config):
    jeffDirPath = os.path.dirname(__file__)
    jeffConfigPath = os.path.join(jeffDirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(jeffConfigPath):
        print('[-] missing configuration file')
        return False

    with open(jeffConfigPath, 'w') as configFile:
        configFile.write(json.dumps(config))

    print('[*] updated configuration file "%s"' % jeffConfigPath)
