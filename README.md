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

_https://github.com/JeffJerseyCow/dockerimages/tree/master/libfuzzer_

### libFuzzer
```jeff libfuzzer``` provides access to the LLVM libFuzzer toolchain
- ```jeff libfuzzer DIR``` copies the contents of DIR into a libFuzzer environment, runs a ```build.sh``` script and executes the output ```fuzz.me```
- ```jeff libfuzzer DIR -c /corpus/dir -a /artifacts/dir``` copies the corpus and/or artifacts directory contents to a directory of your choosing
- ```jeff libfuzzer DIR --no-asan``` turns of address sanitizer

_https://github.com/JeffJerseyCow/dockerimages/tree/master/debug_

## Future
In the future I will add more environments starting with AFL that links against the test harness ```LLVMFuzzerTestOneInput```.

- AFL fuzzer
- PowerPC debugging environment

## Notes
The docker containers recursivley copy the contents of DIR to their internal environments. The bigger it is the longer it takes.
