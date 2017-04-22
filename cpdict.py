#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.cpdict - case preserving case insensitive dict
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

import collections

class CasePreservingDict(collections.MutableMapping):
    """
    Ordered, case-preserving and case-insensitive dict.
    Casing of first write is preserved.
    """
    def __init__(self, data=None, **kwargs):
        self._data = collections.OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def copy(self):
        return CasePreservingDict(self._data.values())

    def __setitem__(self, key, value):
        preservedkey = self._data.get(key.lower(), (key, value))[0]
        self._data[key.lower()] = (preservedkey, value)

    def __getitem__(self, key):
        return self._data[key.lower()][1]

    def __delitem__(self, key):
        del self._data[key.lower()]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return (k for k, v in self._data.values())

    def lower_items(self):
        return ((k, v[1]) for (k, v) in self._data.items())

    def __eq__(self, other):
        if isinstance(other, CasePreservingDict):
            pass
        elif isinstance(other, collections.Mapping):
            other = CasePreservingDict(other)
        else:
            return NotImplemented
        return dict(self.lower_items()) == dict(other.lower_items())

    def __repr__(self):
        return str(dict(self.items()))

