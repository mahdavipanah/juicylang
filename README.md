# JuicyLang
Juicy is an experimental and educational purposed interpreted programming language written in Python using [PLY](http://www.dabeaz.com/ply/).  
  
*This is my compiler course project in university therefore is a good start for anyone who intends to
learn compiler and interpreter design.*

# Installing

### Dependencies
- [Python3.5+](https://www.python.org/)
- [PLY](http://github.com/dabeaz/ply)
- [Colorama](https://github.com/tartley/colorama)

Make sure you have Python on your system and then in order to install
Dependencies go to project's directory and enter this command
```Bash
pip install -r requirements.txt
```

# Usage
```
$ ./juicylang --help
Usage: juicylang [file-name]
    Runs and interprets the given jul file.
    If no file is given, reads from standard input.
    Example usage:
        $ asmrun examples/myprogram.jul
Options:
    -h, --help  Shows help text.
Author:
    Hamidreza Mahdavipanah <h.mahdavipanah@gmail.com>
Repository:
    http://github.com/mahdavipanah/juicylang
License:
    MIT License

```
There are some example programs written in Juicy in [examples directory](./examples).

# License

[MIT](./LICENSE)
