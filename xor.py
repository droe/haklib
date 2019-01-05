#!/usr/bin/env python3
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.xor - building blocks for breaking XOR encrypted ciphertext
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

def xorcrypt(buf, key):
    """
    XOR encrypt/decrypt a buffer with a key.

    >>> xorcrypt(b'1234', b'12')
    b'\\x00\\x00\\x02\\x06'
    >>> xorcrypt(b'12345', b'12')
    b'\\x00\\x00\\x02\\x06\\x04'
    """
    if len(key) == 0:
        return buf
    out = []
    for i in range(0, len(buf)):
        out.append(buf[i] ^ key[i % len(key)])
    return bytes(out)

def ioc(buf, shift):
    """
    Calculate index of coincidence for a specific shift of buf against itself,
    i.e. the number of zeroes resulting from XORing buf against shifted buf.

    >>> ioc(b'\\x01\\x02\\x01\\x02', 2)
    2
    """
    assert shift > 0
    zeroes = 0
    for i in range(0, len(buf) - shift):
        if buf[i] ^ buf[i+shift] == 0:
            zeroes += 1
    return zeroes

def keylen_ioc(buf, shiftrange=(1, 64), limit=0.01):
    """
    Determine the most likely key length of ciphertext buf based on the index
    of coincidence method.  Currently returns the smallest shift with
    frequency over limit.

    >>> keylen_ioc(b'abxabcabcwbcabc')
    3
    """
    for shift in range(*shiftrange):
        zeroes = ioc(buf, shift)
        freq = zeroes / len(buf)
        if freq > limit:
            return shift

def xordiff(buf, period):
    """
    Calculate XOR differentials for the given period (key length).

    >>> xordiff(b'abcdefg', 3)
    b'\\x05\\x07\\x05\\x03'
    """
    out = []
    for base in range(len(buf) - period):
        out.append(buf[base] ^ buf[base + period])
    return bytes(out)

def xorattack_kpt(buf, kpts, keylen=None, mindiffs=3):
    """
    Break the XOR key by looking for XOR differentials of known plaintext.
    If key length (period) is not given, it is calculated using the index of
    coincidence method.  Known plaintexts that result in fewer than mindiffs
    effective XOR differentials are silently skipped in order to prevent FPs.
    Yields candidate (plaintext, key, offset) tuples for examination by the
    caller.

    >>> ct = b'abxabcabcwbcab'
    >>> kpts = [b'wrong', b'\\x1b\\x00\\x00\\x1b\\x16']
    >>> for pt, key, offset in xorattack_kpt(ct, kpts, mindiffs=2):
    ...   if pt[:2] == b'\\x00\\x00':
    ...     continue
    ...   print(pt)
    ...   print(key)
    ...   print(offset)
    ...   break
    b'\\x16\\x00\\x00\\x16\\x00\\x1b\\x16\\x00\\x1b\\x00\\x00\\x1b\\x16\\x00'
    b'wbx'
    8
    """
    if keylen == None:
        keylen = keylen_ioc(buf[:1024*1024])
    buf_d = xordiff(buf, keylen)
    keys = set()
    for kpt in kpts:
        if len(kpt) < keylen + mindiffs:
            continue
        kpt_d = xordiff(kpt, keylen)
        matches = [i for i in range(len(buf_d)) if buf_d.startswith(kpt_d, i)]
        for match in matches:
            key = []
            for i in range(keylen):
                key.append(buf[match+i] ^ kpt[i])
            keyoffset = keylen - (match % keylen)
            if keyoffset < keylen:
                key = key[keyoffset:]+key[:keyoffset]
            key = bytes(key)
            if key not in keys:
                keys.add(key)
                yield (xorcrypt(buf, key), key, match)


if __name__ == '__main__':
    import doctest, sys
    fails, tests = doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    if fails > 0:
        sys.exit(1)
    else:
        sys.exit(0)

