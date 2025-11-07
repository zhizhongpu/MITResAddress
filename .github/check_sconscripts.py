#!/usr/bin/env python3
import os
import re
import sys

def IsExcludedPath(path, excluded=None):
    if excluded is None:
        excluded = ["source/lib", "source/raw"]
    norm = os.path.normpath(path)
    return any(norm == e or norm.startswith(e + os.sep) for e in excluded)

def IsHidden(name):
    return name.startswith(".")

def ReadFile(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return None

def FilesNotMentioned(dir_path, content, filenames):
    missing = []
    for name in sorted(filenames):
        if name == "SConscript":
            continue
        if name not in content:
            missing.append(f"{dir_path} -> {name}")
    return missing

def SubdirsNotMentioned(dir_path, content, subdirs):
    missing = []
    for name in sorted(subdirs):
        pattern = rf"\b{re.escape(name)}\b"
        if not re.search(pattern, content):
            missing.append(f"{dir_path} -> {name}")
    return missing

def CollectSConscriptProblems(root, excluded=None):
    missing_sconscript_dirs = []
    missing_file_mentions = []
    missing_dir_mentions = []
    for dir_path, dir_names, file_names in os.walk(root):
        if IsExcludedPath(dir_path, excluded):
            dir_names[:] = []
            continue
        dir_names[:] = [d for d in dir_names if not IsHidden(d)]
        file_names = [f for f in file_names if not IsHidden(f)]
        if os.path.normpath(dir_path) == os.path.normpath(root):
            continue
        if not dir_names and not file_names:
            continue
        sconscript_path = os.path.join(dir_path, "SConscript")
        content = ReadFile(sconscript_path)
        if content is None:
            missing_sconscript_dirs.append(dir_path)
            continue
        missing_file_mentions.extend(FilesNotMentioned(dir_path, content, file_names))
        missing_dir_mentions.extend(SubdirsNotMentioned(dir_path, content, dir_names))
    return missing_sconscript_dirs, missing_file_mentions, missing_dir_mentions

def TopLevelSourceFolders(root, excluded=None):
    if excluded is None:
        excluded = ["source/lib", "source/raw"]
    try:
        entries = sorted(os.listdir(root))
    except Exception:
        return []
    folders = []
    for e in entries:
        full = os.path.join(root, e)
        if not os.path.isdir(full):
            continue
        if IsHidden(e):
            continue
        if IsExcludedPath(full, excluded):
            continue
        folders.append(e)
    return folders

def SourceFoldersMissingInSConstruct(sconstruct_path="SConstruct", root="source", excluded=None):
    content = ReadFile(sconstruct_path)
    if content is None:
        return TopLevelSourceFolders(root, excluded)
    missing = []
    for folder in TopLevelSourceFolders(root, excluded):
        pattern = rf"\b{re.escape(folder)}\b"
        if not re.search(pattern, content):
            missing.append(folder)
    return missing

def main():
    root = "source"
    excluded = ["source/lib", "source/raw"]
    missing_dirs, missing_files, missing_subdirs = CollectSConscriptProblems(root=root, excluded=excluded)
    missing_in_sconstruct = SourceFoldersMissingInSConstruct("SConstruct", root=root, excluded=excluded)
    any_problems = bool(missing_dirs or missing_files or missing_subdirs or missing_in_sconstruct)
    if any_problems:
        print("SConscript/SConstruct summary of missing items:")
        if missing_dirs:
            print("\nFolders missing SConscript:")
            for p in missing_dirs:
                print(p)
        if missing_files:
            print("\nFiles not mentioned in their SConscript:")
            for p in missing_files:
                print(p)
        if missing_subdirs:
            print("\nSubfolders not mentioned in their parent SConscript:")
            for p in missing_subdirs:
                print(p)
        if missing_in_sconstruct:
            print("\nTop-level source folders missing from root SConstruct:")
            for p in missing_in_sconstruct:
                print(p)
    else:
        print("SConscript/SConstruct summary: all checks passed.")
    return 1 if any_problems else 0

if __name__ == "__main__":
    sys.exit(main())
