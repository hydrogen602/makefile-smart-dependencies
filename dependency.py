#!/usr/bin/env python3

'''
A utility for scanning C code for dependencies and returning them.

It works by recursively looking for the pattern #include "<- anything here ->"
Thus it doesn't care about file endings.

Use -p to print debug logs.

Useful with GNU makefile like

.SECONDEXPANSION:
%.o: %.c $$(shell ./dependency.py %.c)
	@echo $@ $^
'''

from io import TextIOWrapper
from pathlib import Path
import sys
import re
from typing import Optional

include = re.compile(r'^\s*\#include\s+"(.+)"\s*$', re.MULTILINE)

debug = sys.argv[1] == '-p'
if debug:
    sys.argv.pop(1)

code_file = Path(sys.argv[1])

# sub rule


def main(code_file: Path, p: Optional[TextIOWrapper]):
    if not code_file.exists():
        return  # do nothing for now

    headers = set()

    def get_all_deps(file: Path, first: bool = False):
        headers.add(file)
        if not first:
            print(file)
        if p is not None:
            print(file, file=p)
        with file.open('r') as f:
            for m in include.finditer(f.read()):
                dep = Path(m.group(1))
                if dep not in headers:
                    get_all_deps(dep)

    get_all_deps(code_file, first=True)


if debug:
    with Path('output.log').open('a') as p:
        main(code_file, p)
else:
    main(code_file, None)
