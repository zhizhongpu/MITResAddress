#!/usr/bin/env python3
from pathlib import Path

TARGET = "scons: building terminated because of errors."

def Main():
    bad = []
    for p in Path(".").rglob(".log"):
        try:
            if TARGET in p.read_text(errors="replace"):
                bad.append(p)
        except:
            pass

    if not bad:
        print("No sconscript.log files contain the error string.")
        return 0

    print("Problematic sconscript.log files:")
    for p in bad:
        print(" -", p)

    return 1

if __name__ == "__main__":
    Main()
