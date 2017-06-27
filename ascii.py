#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.ascii - has functions for ASCII drawing
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

def asciibox(msg, title=None, minwidth=None):
    """
    Returns message string *msg* wrapped in a plain ASCII box.
    If *width* is given, pad the lines to *width* characters.
    If *title* is given, add *title* in the top horizontal bar.
    """
    out = []
    lines = msg.splitlines()
    width = 0
    for line in lines:
        width = max(width, len(line))
    if minwidth != None:
        width = max(width, minwidth)
    if title != None:
        width = max(width, len(title) + 6)
    ftr = "+" + ("-" * (width + 2)) + "+"
    if title != None:
        hdr = ("+--[ %s ]--" % title) + ("-" * (width - 6 - len(title))) + "+"
    else:
        hdr = ftr
    fmt = "| %%-%is |" % width
    out.append(hdr)
    for line in msg.splitlines():
        out.append(fmt % line)
    out.append(ftr)
    return '\n'.join(out)

