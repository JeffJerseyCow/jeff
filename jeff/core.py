import os
import re
import json
import subprocess

def checkImage(image, config):
    imageVersion = image['version']

    if config['baseDomain'] != '':
        imageName = '%s/%s' % (config['baseDomain'], image['name'])
    else:
        imageName = image['name']

    cmdArgs = ['docker', 'image', 'ls']
    output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout.decode()
    r = re.compile(r'%s\s+%s' % (imageName, imageVersion))

    if not r.search(output):
        cmdArgs = ['docker', 'pull', '%s:%s' % (imageName, imageVersion)]

        try:
            subprocess.run(cmdArgs, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            print('[-] cannot download image %s:%s' % (imageName, imageVersion))
            return False

    return True

def checkDir(directory):
    if not directory:
        return False

    if not os.path.isdir(directory):
        print('[-] directory "%s" doesn\'t exist' % directory)
        return False

    return os.path.realpath(directory)

def checkContainer(args, config):
    cmdArgs = ['docker', 'ps', '-a']
    output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout
    output = output.decode().splitlines()

    for line in output:
        containerName = re.search(r'(\w+)\s*$', line)
        if args.name == containerName.group(0) and args.name in config['containers']:
            cmdArgs = ['docker', 'start', '%s' % args.name]
            subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, check=True)

            cmdArgs = ['docker', 'attach', '%s' % args.name]
            print('[*] loading existing container "%s"' % args.name)
            subprocess.run(cmdArgs)

            return True

    return False

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

def updateVolume(hostDir, guestDir):
    directory = checkDir(hostDir)

    if not directory:
        print('[-] unknown directory "%s"' % hostDir)
        return False

    return ['-v', '%s:%s' % (directory, guestDir)]

def updateEnv(name, value):
    return ['-e', '%s=%s' % (name, value)]

def startContainer(name, config, cmdArgs):
    try:
        config['containers'].append(name)
        updateConfig(config)
        subprocess.run(cmdArgs, check=True)
        return True
        
    except subprocess.CalledProcessError:
        config['containers'].remove(name)
        updateConfig(config)
        print('[-] cannot create container "%s"' % name)
        return False

def removeContainer(name, config):
    cmdArgs = ['docker', 'ps', '-a']
    output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout
    output = output.decode().splitlines()

    for line in output:
        containerName = re.search(r'(\w+)\s*$', line)
        if name == containerName.group(0) and name in config['containers']:
            cmdArgs = ['docker', 'container', 'rm', '--force', '%s' % name]
            subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, check=True)

            # delete from config
            config['containers'].remove(name)
            updateConfig(config)
            return True

    return False
