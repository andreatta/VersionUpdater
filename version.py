#!/usr/bin/env python3
"""
Copyright © 2021 cee cee@ik.me
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

Example of version file:

--- version.c
char VERSION[]     = "0.0.1";
char BUILD_DATE[]  = "xxx";
char GIT_SHA[]     = "xxx";
---

--- version.h
#ifndef VERSION_H
#define VERSION_H

extern char VERSION[];
extern char BUILD_DATE[];
extern char GIT_SHA[];

#endif // VERSION_H
---

"""

import fileinput
import git
import re
import os
from datetime import date

FILENAME     = "version.c"
VERSIONMATCH = "VERSION"
GITMATCH     = "GIT_SHA"
DATEMATCH    = "BUILD_DATE"

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(path, FILENAME)
    print(filepath)
    # Get git short hash
    shashort = ''
    repo = git.Repo(search_parent_directories=True)
    if repo:
        shashort = repo.git.rev_parse(repo.head, short=True)

    # Builddate
    builddate = date.today().strftime("%Y-%m-%d")

    # Regex to find strings surrounded by "
    regex_quotes = re.compile(r"\"(.*)\"")

    # Go through file line by line
    for line in fileinput.FileInput(files=filepath, inplace=True):
        if len(line.strip()) == 0:
            print(line, end='')

        elif line.startswith('#'):
            print(line, end='')

        elif line.find(VERSIONMATCH) > 0:
            version = regex_quotes.findall(line)
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


if __name__ == "__main__":
    main()
