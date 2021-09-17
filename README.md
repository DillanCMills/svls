# svls README

svls is a SystemVerilog Language Server using the [slang](https://sv-lang.com/) project on the backend. Currently, the extension only checks your code for syntax errors. 

## Features

* Checks code for syntax issues
* More coming soon...

## Requirements

svls requires the following dependencies in order to build the slang compiler:

* python 3
* CMake (3.15 or later)
* C++17 compatible compiler

When building slang, add `-DBUILD_SHARED_LIBS=ON` to the cmake command to make sure all the necessary shared libraries are built. 

The server requires the following Python packages (see [requirements.txt](requirements.txt)):
* `pygls`
* `cppyy`

## Extension Settings

This extension contributes the following settings:

* `svls.maxNumberOfProblems`: Controls the maximum number of problems produced by the server
* `svls.trace.server`: Traces the communication between VS Code and the language server
* `svls.slangLibrariesPath`: The path to the lib directory containing the slang compiled shared libraries
* `svls.slangSourceCodePath`: The path to the root of the git repo for the slang source code

## Known Issues

## Release Notes

Please see the [release notes page](RELEASES.md)
