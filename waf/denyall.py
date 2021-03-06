#!/usr/bin/env python

"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re

from lib.core.enums import HTTPHEADER
from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "Deny All Web Application Firewall (DenyAll)"

def detect(get_page):
    page, headers, code = get_page()
    retval = re.search(r"\Asessioncookie=", headers.get(HTTPHEADER.SET_COOKIE, ""), re.I) is not None

    if not retval:
        for vector in WAF_ATTACK_VECTORS:
            page, headers, code = get_page(get=vector)
            retval = code == 200 and re.search(r"\ACondition Intercepted", page, re.I) is not None
            if retval:
                break

    return retval
