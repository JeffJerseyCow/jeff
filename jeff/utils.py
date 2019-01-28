import re
import os
import json
import importlib
import subprocess

def checkDocker():
    """Checks docker is installed and user is a member of the docker group.

    Returns:
        True if docker is installed and user is a member of the docker group
        else False.
    """
    try:
        cmdArgs = ['docker', 'version']
        subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=True)
        return True

    except FileNotFoundError:
        print('Error: Install docker.io or docker ce')
        return False

    except subprocess.CalledProcessError:
        print('Error: Add user %s to docker group' % os.getenv("USER"))
        return False

def checkDockerContainer(name):
    cmdArgs = ['docker', 'ps', '-a']
    output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout
    output = output.decode().splitlines()

    for line in output:
        containerName = re.search(r'([\-a-zA-Z0-9_]+)\s*$', line)

        if name == containerName.group(0):
            return True

    return False

def checkJeffContainer(name, config):
    for containerName in config['containers']:
        if name == containerName:
            return True

    return False

def loadConfig():
    """Loads the jeff confgiruation file.

    Returns:
        The jeff configuration file as a dictionary else False.
    """
    jeffDirPath = os.path.dirname(__file__)
    jeffConfigPath = os.path.join(jeffDirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(jeffConfigPath):
        print('Error: Missing configuration file')
        return False

    with open(jeffConfigPath, 'r') as configFile:
        return json.loads(configFile.read())

def loadPlugins(config):
    """Loads jeff plugins specified in the config file.

    Args:
        config: jeff configuration dictionary loaded with utils.loadConfig.

    Returns:
        A dictionary containing the loaded module indexed by the plugin nameself
        else False.
    """
    plugins = {}
    importPrefix = 'jeff.plugins'

    for name in config['plugins']:
        plugins[name] = importlib.import_module('%s.%s' % (importPrefix, name))

    return plugins

def listContainers(config):
    """Prints current jeff containers.

    Args:
        config: jeff configuration dictionary loaded with utils.loadConfig.

    Returns:
        True
    """
    for container in config['containers']:
        print(container)

    return True

def updateConfig(config):
    """Updates the configuration file with the configuration dictionary config.

    Args:
        config: jeff configuration dictionary loaded with utils.loadConfig.

    Returns:
        True if configuration file was written to successfully else False.
    """
    dirPath = os.path.dirname(__file__)
    configPath = os.path.join(dirPath, 'config', 'jeffconfig.json')

    if not os.path.isfile(configPath):
        print('Error: Missing configuration file')
        return False

    with open(configPath, 'w') as configFile:
        configFile.write(json.dumps(config))
        return True

def removeContainer(name, config):
    """Removes the container specified with name.

    Args:
        name: Name of container to remove.
        config: jeff configuration dictionary loaded with utils.loadConfig.

    Returns:
        True if container was removed else False.
    """
    if checkJeffContainer(name, config) and not checkDockerContainer(name):
        config['containers'].remove(name)
        updateConfig(config)
        print('Deleted invalid jeff entry')
        return True

    elif checkJeffContainer(name, config) and checkDockerContainer(name):
        cmdArgs = ['docker', 'container', 'rm', '--force', '%s' % name]
        subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=True)
        config['containers'].remove(name)
        updateConfig(config)
        print('Deleted %s' % name)
        return True

    print('Error: Container %s does not exist' % name)
    return False
