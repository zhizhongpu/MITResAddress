#!/usr/bin/env python3
import os
import subprocess
import sys

CHECKS = [
    ("SCons DAG", "check_scons"),
    ("Newlines",  "check_newlines"),
    ("EPS data",  "check_eps"),
    ("Build log", "check_scons_log"),
]

def main():
    repo   = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]

    rows   = []
    failed = []

    print("Runtime:")
    for name, step_id in CHECKS:
        key     = step_id.upper()
        outcome = os.environ.get(f"{key}_OUTCOME", "skipped")
        time    = os.environ.get(f"{key}_TIME", "")
        print(f"  {step_id}: {time}s")

        if outcome == "skipped":
            rows.append(f"| {name} | SKIP | |")
        elif outcome == "success":
            rows.append(f"| {name} | ✅ | {time}s |")
        else:
            failed.append(name)
            rows.append(f"| {name} | ❌ | {time}s |")

    pr_num = os.environ.get("PR_NUMBER")
    if pr_num:
        pr_sha      = os.environ["PR_SHA"]
        comment_url = os.environ.get("COMMENT_URL", "")
        run_url     = f"https://github.com/{repo}/actions/runs/{run_id}"

        table   = "\n".join(["| Check | Result | Time |", "|-------|--------|------|", *rows])
        trigger = f" · [requesting comment]({comment_url})" if comment_url else ""
        body    = f"**Check Results** ([run details]({run_url}){trigger})\n\n{table}"

        subprocess.run(["gh", "pr", "comment", pr_num, "--body", body], check=True)

        state = "failure" if failed else "success"
        desc  = f"Failed: {', '.join(failed)}" if failed else "All checks passed"
        subprocess.run([
            "gh", "api", f"repos/{repo}/statuses/{pr_sha}",
            "-f", f"state={state}",
            "-f", "context=Checks",
            "-f", f"description={desc}",
            "-f", f"target_url={run_url}",
        ], check=True)

    if failed:
        print(f"Failed checks: {', '.join(failed)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
