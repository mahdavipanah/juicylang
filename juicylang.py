#!/usr/bin/env python3
"""
juicylang - Juicy programming language written in Python using PLY
Author : Hamidreza Mahdavipanah
Version: 1.0.0
Repository: http://github.com/mahdavipanah/juicylang
License : MIT License
"""
from sys import exit, argv, stdin
from colorama import init as colorama_init, Fore
from src.juicyyacc import yacc

# Initialize colorama
colorama_init(autoreset=True)

# A file has been passed
if len(argv) > 1:
    # Showing help text
    if argv[1] in {'-h', '--help'}:
        print("Usage: juicylang [file-name]\n"
              "    Runs and interprets the given jul file.\n"
              "    If no file is given, reads from standard input.\n"
              "    Example usage:\n"
              "        $ asmrun examples/myprogram.jul\n"
              "Options:\n"
              "    -h, --help  Shows help text.\n"
              "Author:\n"
              "    Hamidreza Mahdavipanah <h.mahdavipanah@gmail.com>\n"
              "Repository:\n"
              "    http://github.com/mahdavipanah/juicylang\n"
              "License:\n"
              "    MIT License")
        exit(0)

    # Reading a source file
    source = ""
    try:
        with open(argv[1], 'rt', encoding='utf-8') as file:
            source = file.read()
    except FileNotFoundError:
        print(Fore.RED + "File '" + Fore.BLACK + argv[1] + Fore.RED + "' not found")
        exit(1)

    yacc.parse(source)
    exit(0)


# Read program's rouce file form standard input
source = ""
for line in stdin:
    source += line

yacc.parse(source)