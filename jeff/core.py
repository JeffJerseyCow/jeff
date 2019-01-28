import os
import re
import subprocess
from jeff.utils import updateConfig, checkDockerContainer, checkJeffContainer

class JeffContainer:

    def __init__(self, image, args, config, privileged=False):
        """Instantiate the JeffContainer class.

        Args:
            image: Image dictionary of the format
                {'name': '{DOCKER_IMAGE_NAME}',
                 'version': '{DOCKER_IMAGE_VERSION}'}.
            args: Arguments parsed with argparse.
            config: jeff configuration dictionary loaded with utils.loadConfig.
            privileged: Flag to indicate if docker container requires privileged
                        access.
        """
        if config['baseDomain'] != '':
            self._imageName = '%s/%s' % (config['baseDomain'], image['name'])
        else:
            self._imageName = image['name']

        self._imageVersion = image['version']
        self._args = args
        self._config = config
        self._privileged = privileged
        self._volumes = []
        self._flags = []

    def addEnv(self, name, value):
        """Create docker environment string of the form {name}={value}.

        Args:
            name: Name of the environment variable to set.
            value: Value of the environment variable to set.

        Returns:
            docker environment string list.
        """
        return ['-e', '%s=%s' % (name, value)]

    def addFlags(self, flags):
        """Create custom flags to the docker string.

        Args:
            flags: List containg the additional flags.

        Returns:
            docker flag string list.
        """
        self._flags = self._flags + flags
        return True

    def addVolume(self, hostDir, guestDir):
        """Create docker volume string of the form {hostDir}/:{guestDir}/.

        Args:
        hostDir: Host directory to mount.
        guestDir: Mount point in the docker container.

        Returns:
        docker volume string list else False if the host directory doesn't
        exists.
        """
        if not hostDir:
            return False

        if not os.path.isdir(hostDir):
            print('Error: Directory %s doesn\'t exist' % hostDir)
            return False

        directory = os.path.realpath(hostDir)
        self._volumes = self._volumes + ['-v', '%s:%s' % (directory, guestDir)]
        return True

    def _addImage(self):
        """Create docker image string of the form
        {BASE_DOMAIN}/{DOCKER_IMAGE_NAM}:{DOCKER_IMAGE_VERSION}.

        Returns:
            docker image string list.
        """
        if self._config['baseDomain'] != '':
            return ['%s/%s:%s' % (self._config['baseDomain'], self._imageName, self._imageVersion)]
        else:
            return ['%s:%s' % (self._imageName, self._imageVersion)]

    def _addJeffEntry(self):
        self._config['containers'].append(self._args.name)
        updateConfig(self._config)

    def _checkDockerContainer(self):
        return checkDockerContainer(self._args.name)

    def _checkJeffContainer(self):
        return checkJeffContainer(self._args.name, self._config)

    def _deleteJeffEntry(self):
        self._config['containers'].remove(self._args.name)
        updateConfig(self._config)

    def _loadJeffContainer(self):
        cmdArgs = ['docker', 'start', '%s' % self._args.name]
        subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, check=True)

        cmdArgs = ['docker', 'attach', '%s' % self._args.name]
        print('Loaded existing container %s' % self._args.name)

        if self._args.directory:
            print('Cannot configure directory for existing container')

        subprocess.run(cmdArgs)
        return True

    def _pullLatest(self):
        if not self._args.no_update:
            cmdArgs = ['docker', 'pull'] + self._addImage()
            try:
                subprocess.run(cmdArgs, check=True)
            except subprocess.CalledProcessError:
                print("Warning: Cannot pull latest image")

    def start(self):
        """Create and run docker container.

        Returns:
        True if container is created and loaded else False.
        """

        # Check for invalid state (JC -> DC)
        if self._checkJeffContainer() and not self._checkDockerContainer():
            print("Warning: jeff is in an invalid state, deleting incorrect entry")
            self._deleteJeffEntry()

        # Check for valid state (JC && DC)
        elif self._checkJeffContainer() and self._checkDockerContainer():
            return self._loadJeffContainer()

        # Check for valid state (¬JC && DC)
        elif not self._checkJeffContainer() and self._checkDockerContainer():
            print("Error: Container name already in use")
            return False

        # Default for valid state (¬JC && ¬DC)
        self._pullLatest()

        cmdArgs = ['docker', 'run', '-ti', '--name', self._args.name,
                   '-h', self._args.name]

        if self._privileged:
            cmdArgs = cmdArgs + ['--privileged']

        cmdArgs = cmdArgs + self.addEnv('INITIALGID', os.getgid())
        cmdArgs = cmdArgs + self.addEnv('INITIALUID', os.getuid())
        cmdArgs = cmdArgs + self._volumes
        cmdArgs = cmdArgs + self._flags
        cmdArgs = cmdArgs + self._addImage()

        self._addJeffEntry()

        if 'directory' in self._args and not self._args.directory:
            print('Directory not specified')

        try:
            subprocess.run(cmdArgs, check=True)
            return True
        except subprocess.CalledProcessError:
            print("Error: Cannot create container, check image and name")

        return False
