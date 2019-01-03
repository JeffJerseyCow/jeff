# jeff
Wrapper for Dynamic Analysis Docker Images

## Requirements
- Docker

*Note: Your user account needs to be a member of the docker group*

```sudo usermod -aG docker $USER```

## Commands
### Config
```jeff config``` configure jeff settings
- ```jeff config --show``` prints current configuration
- ```jeff config --list``` list jeff containers
- ```jeff config --rm RM``` remove containers called RM
- ```jeff config --base-domain BASE_DOMAIN``` set the base domain to BASE_DOMAIN
- ```jeff config --reset-base-domain``` resets the base domain

*Note: The base domain can remain default -- it's configurable for air-gapped network*

### General
- ```jeff debug``` cgdb, gdb, gef, peda
- ```jeff libfuzzer``` fuzzer from llvm 8.0
- ```jeff afl``` latest afl build
- ```jeff ikos``` NASA abstract interpretation  engine

All commands have a mandatory ```--name NAME``` flag and an optional ```-directory DIRECTORY``` flag that maps DIRECTORY into the container.
