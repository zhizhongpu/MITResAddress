#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path

def GetTrackedFiles():
    out = subprocess.run(["git","ls-files"], stdout=subprocess.PIPE, check=True).stdout.decode().splitlines()
    return [Path(p) for p in out if p.strip()]

def IsBinary(path):
    try:
        return b"\0" in path.read_bytes()[:4096]
    except:
        return True

def NeedsNewline(path):
    try:
        data = path.read_bytes()
        return len(data) == 0 or not data.endswith(b"\n")
    except:
        return False

def AddNewline(path):
    path.write_bytes(path.read_bytes() + b"\n")

def StageFiles(paths):
    if paths:
        subprocess.run(["git","add"] + [str(p) for p in paths], check=True)

def CommitIfStaged(msg):
    if subprocess.run(["git","diff","--cached","--quiet"]).returncode == 0:
        return False
    subprocess.run(["git","commit","-m",msg,"--no-verify"], check=True)
    return True

def ProcessFiles(fix):
    tracked = GetTrackedFiles()
    missing = []
    fixed = []
    for p in tracked:
        if not p.exists() or IsBinary(p):
            continue
        if NeedsNewline(p):
            missing.append(p)
            if fix:
                AddNewline(p)
                fixed.append(p)
    if not missing:
        print("No files missing trailing newlines.")
        return 0
    print("Files missing trailing newline:")
    for p in missing:
        print(" -", p)
    if not fix:
        return 0
    StageFiles(fixed)
    if CommitIfStaged("[github-actions] Add missing newlines"):
        print("Committed fixes for:", ", ".join(str(p) for p in fixed))
    else:
        print("No changes staged/committed.")
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", choices=["yes","no"], default="no")
    args = parser.parse_args()
    return ProcessFiles(args.fix=="yes")

if __name__ == "__main__":
    raise SystemExit(main())
