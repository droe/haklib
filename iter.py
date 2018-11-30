#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.iter - n-wise grouped iterators
# Copyright (C) 2018, Daniel Roethlisberger <daniel@roe.ch>
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


from itertools import zip_longest


def pairwise(iterable):
    """
    Return elements in *iterable* in pairs of two.
    Does not return the last `len(iterable) % 2` elements.
    """
    it = iter(iterable)
    return zip(it,it)


def chunkwise(iterable, chunksize=2):
    """
    Return elements in *iterable* in chunks of *chunksize*.
    Does not return the last `len(iterable) % chunksize` elements.
    """
    it = iter(iterable)
    return zip(*[it]*chunksize)


def blockwise(iterable, blocksize=2, fillvalue=None):
    """
    Return elements in *iterable* in blocks of *blocksize*.
    Returns all elements; fills the last block with
    `blocksize - (len(iterable) % blocksize)` times *fillvalue*.
    """
    it = iter(iterable)
    return zip_longest(*[it]*blocksize, fillvalue=fillvalue)

