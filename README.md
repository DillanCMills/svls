# svls README

svls is a SystemVerilog Language Server using the [slang](https://sv-lang.com/) project on the backend. Currently, the extension only checks your code for syntax errors. 

## Features

* Checks code for syntax issues

## Requirements

svls requires the following dependencies in order to build the slang compiler used internally:

* python 3
* CMake (3.15 or later)
* C++17 compatible compiler

## Extension Settings

This extension contributes the following settings:

* `svls.enable`: enable/disable this extension
* `svls.pythonPath`: If Python 3 is not found in your path, use this to point to it
* `svls.cmakePath`: If CMake is not found in your path, use this to point to it
* `svls.cppPath`: If a compatible C++ compiler is not found in your path, use this to point to it
* `svls.cmakeFlags`: Set to override the default slang cmake arguments
* `svls.makeFlags`: Set to override the default slang make arguments
* `svls.slangLibraries`: If you already have the slang shared libraries on your machine, use this to point to them

## Known Issues

## Release Notes

Please see the [release notes page](RELEASES.md)
