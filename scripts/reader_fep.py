#!/usr/bin/python

import sys

if "reader" in sys.argv[0]: # CHANGE: handle case sys.argv == ./reader

    from bbciot.reader import RunReader
    RunReader(1500)

if "FEP" in sys.argv[0]: # CHANGE: handle case sys.argv == ./FEP

    from bbciot.collator import RunCollator
    RunCollator()
