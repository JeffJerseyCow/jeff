# jeff
Wrapper for Dynamic Analysis Docker Images

## Requirements
- Docker

_Note: Your user account needs to be a member of the docker group_

```sudo usermod -aG docker $USER```

## Commands
### Config
```jeff config``` provides access to the configuration file
- ```jeff config --show``` prints current configuration
- ```jeff config -b example.com``` changes the base domain
- ```jeff config --reset-base-domain``` resets the base domain

### Debug
```jeff debug``` provides access to a debugging environment
- ```jeff debug DIR``` copies the contents of DIR into a debugging environment

### libFuzzer
```jeff libfuzzer``` provides access to the LLVM libFuzzer toolchain
- ```jeff libfuzzer DIR``` copies the contents of DIR into a libFuzzer environment, runs a ```build.sh``` script and executes the output ```fuzz.me```
- ```jeff libfuzzer DIR -c /corpus/dir -a /artifacts/dir``` optionally copies the corpus and/or artifacts directory contents to a directory of your choice

