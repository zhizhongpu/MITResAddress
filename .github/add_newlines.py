#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path

EXCLUDED_EXT = {".log", ".txt"}
OUTFILE = Path(".github/newlines_to_commit.txt")

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

def AddNewline(p): p.write_bytes(p.read_bytes()+b"\n")

def ProcessFiles(fix):
    OUTFILE.unlink(missing_ok=True)
    missing = [p for p in GetTrackedFiles() if p.exists() and p.suffix not in EXCLUDED_EXT and not IsBinary(p) and NeedsNewline(p)]
    if not missing:
        print("No files missing trailing newlines."); return 0
    print("Files missing trailing newline:")
    for p in missing: print(" -", p)
    if not fix: return 0
    for p in missing: AddNewline(p)
    OUTFILE.write_text("\n".join(str(p) for p in missing))
    print("Wrote fixes list to", OUTFILE)
    return 0

def Main():
    p = argparse.ArgumentParser()
    p.add_argument("--fix", choices=["yes","no"], default="no")
    args = p.parse_args()
    return ProcessFiles(args.fix=="yes")

if __name__=="__main__": 
    Main()
