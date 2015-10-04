#!/usr/bin/env python2
#
# weeman.py - HTTP server for phishing
#
#  Weeman is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Weeman is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Hypsurus <hypsurus@mail.ru>
#

import sys
from core.misc import printt

def tests_pyver():
    if sys.version[:3] == "2.7" or "2" in sys.version[:3]:
        pass # All good
    elif "3" in sys.version[:3]:
        printt(1,"Weeman has no support for Python 3.")
    else:
        printt(1, "Your Python version is very old ..")

def tests_platform():
    if "linux" in sys.platform:
        printt(3, "Running Weeman on linux ... (All good)")
    elif "darwin" in sys.platform:
        printt(3, "Running Weeman on \'Mac\' (All good)")
    elif "win" in sys.platform:
        printt(3, "Running Weeman on \'Windows\' (Not tested)")
    else:
        printt(3, "If \'Weeman\' runs sucsessfuly on your platform %s\nPlease let me (@Hypsurus) know!" %sys.platform)

def main():
    tests_pyver()
    tests_platform()
    try:
        from bs4 import BeautifulSoup as bs
    except ImportError:
        printt(1, "Please install beautifulsoup 4 to continue ...")
    from core.shell import shell
    shell()

if __name__ == '__main__':
    main()
