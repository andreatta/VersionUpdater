#!/usr/bin/env python3
"""
Copyright © 2021 cee
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

Install packages:
```
pip install gitpython
```

Example of version file:

--- version.h
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#ifndef VERSION
#define VERSION    "0.3.2"
#endif

#ifndef VERSIONHEX
#define VERSIONHEX 0x000302
#endif

#ifndef BUILD_DATE
#define BUILD_DATE "2022-02-02"
#endif

#ifndef GIT_SHA
#define GIT_SHA    "ceecee3"
#endif

#ifdef __cplusplus
}
#endif
---

"""

import fileinput
import git
import re
import os
from datetime import date

FILEPATH = ""
FILENAME = "version.h"
IFNDEF = "ifndef"
VERSIONMATCH = "VERSION"
VERSIONHEXMATCH = "VERSIONHEX"
GITMATCH = "GIT_SHA"
DATEMATCH = "BUILD_DATE"
DEBUG = False


def versionsplit(version):    
    v_array = []
    
    if len(version) > 0:
        v_array = version[-1].split('.')
        
        if len(v_array) >= 3:
            build = int(v_array[-1])
            minor = int(v_array[-2])
            major = int(v_array[-3])

            if build < 0xff:
                build += 1
            else:
                build = 0
                if minor < 0xff:
                    minor += 1
                else:
                    minor = 0
                    major += 1

            v_array[-1] = build
            v_array[-2] = minor
            v_array[-3] = major
        
    return v_array


def main():
    print("*** Version Updater ***")

    path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(path, FILEPATH, FILENAME)
    print(filepath)

    if os.path.isdir('.git'):
        # Get git short hash
        repo = git.Repo(search_parent_directories=True)
        shashort = repo.git.rev_parse(repo.head, short=True)
    else:
        shashort = "NOT A GIT REPO"

    # Builddate
    builddate = date.today().strftime("%Y-%m-%d")

    # Regex to find strings surrounded by "
    regex_quotes = re.compile(r"\"(.*)\"")
    regex_hex = re.compile(r"0x\d*")
    v_array = []

    # Go through file line by line
    for line in fileinput.FileInput(files=filepath, inplace=not DEBUG):
        if len(line.strip()) == 0:
            print(line, end='')
            
        elif line.find(IFNDEF) > 0:
            print(line, end='')
                                        
        elif line.find(VERSIONHEXMATCH) > 0:
            versionlist = regex_hex.findall(line)     
            if len(v_array) and len(versionlist):
                versionhex = ["%02x" %i for i in v_array]
                new_version = ''.join(versionhex)
                line = regex_hex.sub('0x' + new_version, line)
                print(line, end='')
            
        elif line.find(VERSIONMATCH) > 0:
            version = regex_quotes.findall(line)
            v_array = versionsplit(version)
            new_version = '.'.join(str(i) for i in v_array)
            line = regex_quotes.sub('"' + new_version + '"', line)
            print(line, end='')            

        elif line.find(GITMATCH) > 0:
            line = regex_quotes.sub('"' + shashort + '"', line)
            print(line, end='')

        elif line.find(DATEMATCH) > 0:
            line = regex_quotes.sub('"' + builddate + '"', line)
            print(line, end='')

        else:
            print(line, end='')


if __name__ == "__main__":
    main()
