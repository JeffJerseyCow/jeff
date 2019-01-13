import re
import os
import json
import importlib
import subprocess

def checkDocker():
    try:
        cmdArgs = ['docker', 'version']
        subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=True)
        return True
    except FileNotFoundError:
        print('Error: Install docker.io or docker ce')
    except subprocess.CalledProcessError:
        print('Error: Add user %s to docker group' % os.getenv("USER"))
        return False

def loadConfig():
    jeffDirPath = os.path.dirname(__file__)
    jeffConfigPath = os.path.join(jeffDirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(jeffConfigPath):
        print('Error: Missing configuration file')
        return False

    with open(jeffConfigPath, 'r') as configFile:
        return json.loads(configFile.read())

def loadPlugins(config):
    plugins = {}
    importPrefix = 'jeff.plugins'

    for name in config['plugins']:
        plugins[name] = importlib.import_module('%s.%s' % (importPrefix, name))

    return plugins

def listContainers(config):
    for container in config['containers']:
        print(container)

    return True

def updateConfig(config):
    dirPath = os.path.dirname(__file__)
    configPath = os.path.join(dirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(configPath):
        print('Error: Missing configuration file')
        return False

    with open(configPath, 'w') as configFile:
        configFile.write(json.dumps(config))

def removeContainer(name, config):
    cmdArgs = ['docker', 'ps', '-a']
    output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout
    output = output.decode().splitlines()

    for line in output:
        containerName = re.search(r'([\-a-zA-Z0-9_]+)\s*$', line)
        if name == containerName.group(0) and name in config['containers']:
            cmdArgs = ['docker', 'container', 'rm', '--force', '%s' % name]
            subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, check=True)

            # delete from config
            config['containers'].remove(name)
            updateConfig(config)

            print('Deleted %s' % name)
            return True

    print('Error: Container %s does not exist' % name)
    return False
