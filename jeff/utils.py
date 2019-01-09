import os
import json
import importlib
import subprocess

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

def checkDocker():
    try:
        cmdArgs = ['docker', 'version']
        subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=True)
        return True
    except FileNotFoundError:
        print('Error: Install docker.io or docker ce')
    except subprocess.CalledProcessError:
        print('Error: Add user "%s" to docker group' % os.getenv("USER"))
    return False
