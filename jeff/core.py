import os
import re
import json
import subprocess
from jeff.utils import updateConfig

class JeffContainer:

    def __init__(self, image, args, config, privileged=False):
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

    def _addImage(self):
        if self._config['baseDomain'] != '':
            return ['%s/%s:%s' % (self._config['baseDomain'], self._imageName, self._imageVersion)]
        else:
            return ['%s:%s' % (self._imageName, self._imageVersion)]

    def _addEnv(self, name, value):
        return ['-e', '%s=%s' % (name, value)]

    def addVolume(self, hostDir, guestDir):
        if not hostDir:
            return False

        if not os.path.isdir(hostDir):
            print('Error: Directory %s doesn\'t exist' % hostDir)
            return False

        directory = os.path.realpath(hostDir)
        self._volumes = self._volumes + ['-v', '%s:%s' % (directory, guestDir)]
        return True

    def addFlags(self, flags):
        self._flags = self._flags + flags
        return True

    def start(self):
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
