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

#ifndef BUILD_DATE
#define BUILD_DATE "2021-11-03"
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

FILEPATH     = ""
FILENAME     = "version.h"
VERSIONMATCH = "VERSION"
GITMATCH     = "GIT_SHA"
DATEMATCH    = "BUILD_DATE"
DEBUG        = False

def main():
    print("Version Updater")

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

    # Go through file line by line
    for line in fileinput.FileInput(files=filepath, inplace=not DEBUG):
        if len(line.strip()) == 0:
            print(line, end='')

        elif line.find(VERSIONMATCH) > 0:
            version = regex_quotes.findall(line)
            if len(version) > 0:
                v_array = version[-1].split('.')
                v_array[-1] = str(int(v_array[-1]) + 1)        
                new_version = '.'.join(v_array)
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
