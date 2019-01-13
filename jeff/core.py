import os
import re
import subprocess
from jeff.utils import updateConfig

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

    def checkImage(self):
        """Check host machine for docker image and pull if not found.

        Returns:
            True if the docker image was found or downloaded successfully else
            False.
        """
        cmdArgs = ['docker', 'image', 'ls']
        output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout.decode()
        r = re.compile(r'%s\s+%s' % (self._imageName, self._imageVersion))

        if not r.search(output):
            cmdArgs = ['docker', 'pull', '%s:%s' % (self._imageName, self._imageVersion)]

            try:
                subprocess.run(cmdArgs, stderr=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError:
                print('Error: Cannot download image %s:%s' % (self._imageName, self._imageVersion))
                return False

        return True

    def checkContainer(self):
        """Check host machine for existing container with the specified
        self._name and load if found.

        Returns:
            True if found and loaded else False.
        """
        cmdArgs = ['docker', 'ps', '-a']
        output = subprocess.run(cmdArgs, check=True, stdout=subprocess.PIPE).stdout
        output = output.decode().splitlines()

        for line in output:
            containerName = re.search(r'([\-a-zA-Z0-9_]+)\s*$', line)

            if self._args.name == containerName.group(0) and self._args.name in self._config['containers']:
                cmdArgs = ['docker', 'start', '%s' % self._args.name]
                subprocess.run(cmdArgs, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, check=True)

                cmdArgs = ['docker', 'attach', '%s' % self._args.name]
                print('Loaded existing container %s' % self._args.name)

                if self._args.directory:
                    print('Cannot configure directory for existing container')

                subprocess.run(cmdArgs)
                return True

        return False

    def _addEnv(self, name, value):
        """Create docker environment string of the form {name}={value}.

        Args:
            name: Name of the environment variable to set.
            value: Value of the environment variable to set.

        Returns:
            docker environment string list.
        """
        return ['-e', '%s=%s' % (name, value)]

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

    def addFlags(self, flags):
        """Create custom flags to the docker string.

        Args:
            flags: List containg the additional flags.

        Returns:
            docker flag string list.
        """
        self._flags = self._flags + flags
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

    def start(self):
        """Create and run docker container.

        Returns:
            True if container is created and loaded else False.
        """
        cmdArgs = ['docker', 'run', '-ti', '--name', self._args.name,
                   '-h', self._args.name]

        if self._privileged:
            cmdArgs = cmdArgs + ['--privileged']

        cmdArgs = cmdArgs + self._addEnv('INITIALGID', os.getgid())
        cmdArgs = cmdArgs + self._addEnv('INITIALUID', os.getuid())
        cmdArgs = cmdArgs + self._volumes
        cmdArgs = cmdArgs + self._flags
        cmdArgs = cmdArgs + self._addImage()

        try:
            self._config['containers'].append(self._args.name)
            updateConfig(self._config)

            if 'directory' in self._args and not self._args.directory:
                print('Directory not specified')

            subprocess.run(cmdArgs, check=True)
            return True

        except subprocess.CalledProcessError:
            self._config['containers'].remove(self._args.name)
            updateConfig(self._config)
            print('Error: Cannot create container %s' % self._args.name)
            return False
