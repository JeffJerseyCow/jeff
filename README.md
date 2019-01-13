# jeff
Wrapper for Dynamic Analysis Docker Images

## Requirements
- Docker

*Note: Your user account needs to be a member of the docker group*

```sudo usermod -aG docker $USER```

## Commands
### Default
- ```jeff --list``` list jeff containers
- ```jeff --remove {RM}``` remove container {RM}

### Config
```jeff config``` configure jeff settings
- ```jeff config --show``` prints current configuration
- ```jeff config --base-domain {BASE_DOMAIN}``` set the base domain to {BASE_DOMAIN}
- ```jeff config --reset-base-domain``` resets the base domain

*Note: The base domain can remain default -- it's configurable for air-gapped network*

### General
- ```jeff debug``` cgdb, gdb, gef, peda
- ```jeff libfuzzer``` fuzzer from llvm 8.0
- ```jeff afl``` latest afl build
- ```jeff ikos``` nasa abstract interpretation  engine
- ```jeff qsym``` qsym concolic execution engine
- ```jeff afl-ppc``` afl qemu configured for PowerPC target
- ```jeff debug-ppc``` gdb-ppc script for PowerPc target

All commands have a mandatory ```--name {NAME}``` flag and an optional ```--directory {DIRECTORY}``` flag that maps DIRECTORY into the container.

## Install
Git clone the repository and use ```pip3 install . --upgrade``` within the source jeff directory.

## Licensing
Contributions to jeff operate under the [MIT](https://github.com/JeffJerseyCow/jeff/blob/master/LICENSE) license.
