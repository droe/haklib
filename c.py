#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.c - helper functions for porting low-level c code to python
# Copyright (C) 2017, Daniel Roethlisberger <daniel@roe.ch>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math

def c_div(q, d):
    """
    Arbitrary signed integer division with c behaviour.

    >>> (c_div(10, 3), c_div(-10, -3), c_div(-10, 3), c_div(10, -3))
    (3, 3, -3, -3)
    >>> c_div(-11, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError
    """
    s = int(math.copysign(1, q) * math.copysign(1, d))
    return s * int(abs(q) / abs(d))

def c_schar(i):
    """
    Convert arbitrary integer to c signed char type range as if casted in c.

    >>> c_schar(0x12345678)
    120
    >>> (c_schar(-128), c_schar(-129), c_schar(127), c_schar(128))
    (-128, 127, 127, -128)
    """
    return ((i + 128) % 256) - 128

def c_uchar(i):
    """
    Convert arbitrary integer to c unsigned char type range as if casted in c.

    >>> c_uchar(0x12345678)
    120
    >>> (c_uchar(-123), c_uchar(-1), c_uchar(255), c_uchar(256))
    (133, 255, 255, 0)
    """
    return i & 0xFF

def c_rot32(i, n):
    """
    Rotate *i* left by *n* bits within the uint32 value range.

    >>> c_rot32(0xF0000000, 4)
    15
    >>> c_rot32(0xF0, -4)
    15
    """
    if n < 0:
        n = 32 + n
    return (((i << n) & 0xFFFFFFFF) | (i >> (32 - n)))

def c_add32(a, b):
    """
    Add *a* and *b* within the uint32 value range.

    >>> c_add32(0xFFFFFFFF, 1)
    0
    >>> c_add32(0xFFFFFFFF, 0xFFFFFFFF)
    4294967294
    """
    return (a + b) & 0xFFFFFFFF

def c_sum32(*args):
    """
    Add all elements of *args* within the uint32 value range.

    >>> c_sum32(0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF)
    4294967293
    """
    return sum(args) & 0xFFFFFFFF



if __name__ == '__main__':
    import doctest, sys
    fails, tests = doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    if fails > 0:
        sys.exit(1)
    else:
        sys.exit(0)

