# haklib - library of possibly reusable python hacks

Copyright (C) 2016-2019, [Daniel Roethlisberger](//daniel.roe.ch/).

## Synopsis

    cd $project
    mkdir -p lib
    git clone https://github.com/droe/haklib.git lib/haklib
    cat >>example.py <<EOF
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/lib')
    import haklib.example
    EOF

## Description

haklib is a collection of individual python modules covering basic standard
functionality that I had to reinvent too many times already.  Everything is
unpolished, incompletely documented and not for the faint of heart.  No API
stability guarantees whatsoever.  Scope of the library is basic
domain-independent functionality that you would expect to be part of a standard
library.  It is mainly intended for my own use but feel free to use and extend.

## Modules

-   **ascii** has functions for ASCII drawing
-   **c** has helper functions for porting low-level c code to python
-   **cpdict** has a case-preserving, case-insensitive dict
-   **dt** has missing datetime functionality such as timezone-aware parsing
    of ISO 8601 timestamps
-   **hexdump** has various conversions to hex, including the python version
    of the venerable `hexdump -C`
-   **iter** has n-wise grouped iterators
-   **pb** has macOS pasteboard (clipboard) access
-   **retry** has a generic retry decorator with exponential backoff and
    filtering
-   **xor** has building blocks for breaking XOR encrypted ciphertext

## Support

There is no support whatsoever.  No communication except in the form of pull
requests fixing bugs or adding features.  You are on your own.

## License

Source code provided under a 2-clause BSD license.

