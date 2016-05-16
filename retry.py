#!/usr/bin/env python
# vim: set list et ts=8 sts=4 sw=4 ft=python:

# haklib.retry - retry decorator with exponential backoff
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

from functools import wraps
from time import sleep

# eclass is the exception class that will trigger a retry.  If the efilter
# function is given, a retry will only be triggered if efilter(e) returns True.
# There will be a maximum of max_retries retries with an exponentially
# increasing delay of (delay * (base ** (retry_count - 1))) seconds.
#
# Example use, retrying for HTTP status 504 but not other errors:
#
#     from haklib.retry import retry
#     @retry(requests.exceptions.HTTPError,
#            lambda e: e.response.status_code in [504])
#     def send_request(self, path):
#         # ...

def retry(eclass, efilter=None, max_retries=8, delay=1, base=2):
    def retry(func):
        @wraps(func)
        def exp_backoff_retry_wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count <= max_retries:
                try:
                    rv = func(*args, **kwargs)
                    break
                except eclass as e:
                    if efilter and not efilter(e):
                        raise
                    if retry_count == max_retries:
                        raise
                    sleep(delay * (base ** retry_count))
                    retry_count += 1
            return rv
        return exp_backoff_retry_wrapper
    return retry

