#!/usr/bin/env python3

import sys

import json


def load_proc(fname):
    with open(fname) as f:
        jf = json.load(f)
        hits = jf["result"]["hits"]["hit"]
        for h in hits:
            h = h["info"]
            if h["type"] == "Conference and Workshop Papers":
                print(h["title"])


if __name__ == "__main__":
    assert len(sys.argv) == 2
    load_proc(sys.argv[1])
