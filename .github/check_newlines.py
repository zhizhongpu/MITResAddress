#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

EXCLUDED_EXT = {".log", ".txt"}

def GetTrackedFiles():
    return [Path(p) for p in subprocess.run(["git","ls-files"], stdout=subprocess.PIPE, check=True).stdout.decode().splitlines() if p.strip()]

def IsBinary(p):
    try:
        return b"\0" in p.read_bytes()[:4096]
    except:
        return True

def NeedsNewline(p):
    try:
        d = p.read_bytes()
        return len(d)==0 or not d.endswith(b"\n")
    except:
        return False

def ProcessFiles():
    missing = [p for p in GetTrackedFiles() if p.exists() and p.suffix not in EXCLUDED_EXT and not IsBinary(p) and NeedsNewline(p)]
    if not missing:
        print("No files missing trailing newlines."); return 0
    print("Files missing trailing newline:")
    for p in missing: print(" -", p)
    return 1

def Main():
    return ProcessFiles()

if __name__=="__main__":
    sys.exit(Main())