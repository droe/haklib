#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.isodt - ISO 8601 related datetime functionality
# Copyright (C) 2016, Daniel Roethlisberger <daniel@roe.ch>
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

import datetime
import re

# Simple timezone info class for UTC
class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

# List of known timezone names
# Note that only timezones with fixed UTC offset are supported.
TZm = {
    'Z':    0,
    'GMT':  0,
    'UTC':  0,
    'CET':  60,
    'CEST': 120,
    # ...
}

# timezone string to datetime.timedelta conversion
def tzs2td(tzs):
    if tzs in TZm:
        return datetime.timedelta(minutes=TZm[tzs])
    if tzs[0] == '-':
        sign = -1
    else:
        sign = 1
    h = int(tzs[1:3])
    m = int(tzs[3:5])
    return datetime.timedelta(minutes=(sign*h*60+m))

# Parse ISO8601-ish timestamp string with timezone; microseconds are ignored
def parse_iso8601(timestamp):
    stamp = re.sub(r' *?([+-][0-9]+|[A-Z]+)$', "", timestamp)
    zone = re.sub(r'^.*?([+-][0-9]+|[A-Z]+)$', "\\1", timestamp)
    dt = datetime.datetime(*map(int, re.split('\D', stamp)[0:6]))
    dt = dt - tzs2td(zone)
    return dt.replace(tzinfo=UTC())

if __name__ == '__main__':
    def _test(dt):
        refstr = '2016-01-06 08:02:04+00:00'
        if not str(dt) == refstr:
            print("%s != %s" % (str(dt), refstr))
    _test(parse_iso8601('2016-01-06 09:02:04 +0100'))
    _test(parse_iso8601('2016-01-06 07:02:04 -0100'))
    _test(parse_iso8601('2016-01-06 08:02:04 UTC'))
    _test(parse_iso8601('2016-01-06T08:02:04Z'))
    _test(parse_iso8601('2016-01-06 10:02:04 CEST'))
    _test(parse_iso8601('2016-01-06 09:02:04.123 CET'))

