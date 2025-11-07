#!/usr/bin/env python3
import os
import re
import sys

def IsExcludedPath(path, excluded):
    norm = os.path.normpath(path)
    return any(norm == e or norm.startswith(e + os.sep) for e in excluded)

def IsHidden(name):
    return name.startswith(".")

def IsIgnoredDir(name):
    return IsHidden(name) or name == "__pycache__"

def IsAllowedPaperFile(name):
    return name.endswith((".bib", ".tex", ".lyx"))

def ReadFile(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return None

def ShouldCheckFile(dir_path, name):
    if os.path.normpath(dir_path).startswith(os.path.normpath(os.path.join("source", "paper"))):
        return IsAllowedPaperFile(name)
    return True

def FilesNotMentioned(dir_path, content, filenames, root):
    missing = []
    rel_dir = os.path.relpath(dir_path, root).replace(os.sep, "/")
    for name in sorted(filenames):
        if name == "SConscript":
            continue
        if not ShouldCheckFile(dir_path, name):
            continue
        stem = os.path.splitext(name)[0]
        canonical_full = ("source/" + rel_dir + "/" + name).lstrip("./")
        canonical_full_noext = ("source/" + rel_dir + "/" + stem).lstrip("./")
        patterns = [
            rf"#{re.escape(name)}",
            rf"#{re.escape(rel_dir + '/' + name)}",
            rf"#{re.escape(canonical_full)}",
            rf"\b{re.escape(name)}\b",
            rf"\b{re.escape(stem)}\b",
            rf"{re.escape(rel_dir + '/' + stem)}",
            rf"{re.escape(canonical_full_noext)}",
        ]
        if not any(re.search(p, content) for p in patterns):
            missing.append(f"{dir_path} -> {name}")
    return missing

def CheckSubdirFilesMentioned(parent_content, subdir_name, subdir_full, root):
    try:
        entries = sorted(os.listdir(subdir_full))
    except Exception:
        return None
    files_to_check = []
    for e in entries:
        full = os.path.join(subdir_full, e)
        if os.path.isdir(full):
            continue
        if IsIgnoredDir(e):
            continue
        if ShouldCheckFile(subdir_full, e):
            files_to_check.append(e)
    if not files_to_check:
        return []
    rel = os.path.relpath(subdir_full, root).replace(os.sep, "/")
    canonical_root_path_slash = ("source/" + rel).lstrip("./")
    missing = []
    for f in sorted(files_to_check):
        stem = os.path.splitext(f)[0]
        patterns = [
            rf"#{re.escape(f)}",
            rf"#{re.escape(subdir_name + '/' + f)}",
            rf"#{re.escape(canonical_root_path_slash + '/' + f)}",
            rf"\b{re.escape(f)}\b",
            rf"\b{re.escape(stem)}\b",
            rf"{re.escape(subdir_name + '/' + stem)}",
            rf"{re.escape(canonical_root_path_slash + '/' + stem)}",
        ]
        if not any(re.search(p, parent_content) for p in patterns):
            missing.append(f)
    return missing

def SubdirsNotMentioned(dir_path, content, subdirs, root, excluded):
    missing = []
    for name in sorted(subdirs):
        if IsIgnoredDir(name):
            continue
        if re.search(rf"\b{re.escape(name)}\b", content):
            continue
        subdir_full = os.path.join(dir_path, name)
        missing_files = CheckSubdirFilesMentioned(content, name, subdir_full, root)
        if missing_files is None:
            missing.append(f"{dir_path} -> {name}")
            continue
        if not missing_files:
            continue
        for f in missing_files:
            missing.append(f"{dir_path} -> {name}/{f}")
    return missing

def CollectSConscriptProblems(root, excluded):
    missing_sconscript_dirs = []
    missing_file_mentions = []
    missing_dir_mentions = []
    for dir_path, dir_names, file_names in os.walk(root):
        if IsExcludedPath(dir_path, excluded):
            dir_names[:] = []
            continue
        dir_names[:] = [d for d in dir_names if not IsIgnoredDir(d)]
        file_names = [f for f in file_names if not IsIgnoredDir(f)]
        if os.path.normpath(dir_path) == os.path.normpath(root):
            continue
        if not dir_names and not file_names:
            continue
        sconscript_path = os.path.join(dir_path, "SConscript")
        content = ReadFile(sconscript_path)
        if content is None:
            parent_dir = os.path.dirname(dir_path)
            parent_sconscript = os.path.join(parent_dir, "SConscript")
            parent_content = ReadFile(parent_sconscript)
            if parent_content is None:
                missing_sconscript_dirs.append(dir_path)
                continue
            subdir_name = os.path.basename(dir_path)
            missing_files = CheckSubdirFilesMentioned(parent_content, subdir_name, dir_path, root)
            if missing_files is None:
                missing_sconscript_dirs.append(dir_path)
                continue
            if not missing_files:
                continue
            for f in missing_files:
                missing_file_mentions.append(f"{parent_dir} -> {subdir_name}/{f}")
            continue
        missing_file_mentions.extend(FilesNotMentioned(dir_path, content, file_names, root))
        missing_dir_mentions.extend(SubdirsNotMentioned(dir_path, content, dir_names, root, excluded))
    return missing_sconscript_dirs, missing_file_mentions, missing_dir_mentions

def TopLevelSourceFolders(root, excluded):
    try:
        entries = sorted(os.listdir(root))
    except Exception:
        return []
    folders = []
    for e in entries:
        full = os.path.join(root, e)
        if not os.path.isdir(full):
            continue
        if IsIgnoredDir(e):
            continue
        if IsExcludedPath(full, excluded):
            continue
        folders.append(e)
    return folders

def SourceFoldersMissingInSConstruct(sconstruct_path, root, excluded):
    content = ReadFile(sconstruct_path)
    if content is None:
        return TopLevelSourceFolders(root, excluded)
    missing = []
    for folder in TopLevelSourceFolders(root, excluded):
        if not re.search(rf"\b{re.escape(folder)}\b", content):
            missing.append(folder)
    return missing

def main():
    root = "source"
    excluded = ["source/lib", "source/raw", "source/scrape"]
    missing_dirs, missing_files, missing_subdirs = CollectSConscriptProblems(root, excluded)
    missing_in_sconstruct = SourceFoldersMissingInSConstruct("SConstruct", root, excluded)
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
            print("\nSubfolders or files missing in parent SConscript:")
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
