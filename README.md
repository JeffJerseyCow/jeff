# jeff
Wrapper for Dynamic Analysis Docker Images

This is a quick and dirty shell script that wraps the ```docker run`` images for dynamic analysis.

## Requirements
- docker
- access to jeffjerseycow/llvm:8.0 image
- access to jeffjerseycow/libfuzzer:v0.0.2
- access to jeffjerseycow/debug:v0.0.1

## Fuzz
The fuzz mode takes a directory path as its second positional argument which must contain all source code and a ```build.sh``` script that outputs an libFuzzer executable ```fuzz.me```. For more guidance see https://github.com/JeffJerseyCow/dockerimages/tree/master/libFuzzer

## Examples
Install and simply type ```jeff debug ~/directory``` or ```jeff fuzz ~/directory```

In both cases a new shell is spawed with a copy of the contents ```~/directory```

The debug image requires access to the ```--privileged``` argument as process debugging must be capable ot disabling ASLR.

fuzzer has the aditional optional arguments ```-a ~/artifacts/directory``` and ```-c ~/corpus/directory``` to easily copy corpus and crash artifacts between your local machine and image. For instance:
- ```jeff -a /tmp/artifacts -c /tmp/corpus fuzz ~/directory```

_Note that the optional arguments must precede the operation modes ```fuzz``` or ```debug``` on the command line._
