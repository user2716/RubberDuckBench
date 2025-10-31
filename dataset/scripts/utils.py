import argparse
import json
import os
import subprocess
import sys

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import TerminalFormatter

def run_command(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    return result.stdout.strip()

def info_validate(repo_path, sample_num):
    if not os.path.exists(repo_path):
        print(f"[!] Repo not found at {repo_path}. Run clone")
        sys.exit(1)

    if not is_checked_out(repo_path, sample_num):
        print(f"[!] Run checkout on the sample num you want info for")
        sys.exit(1)


def get_file_src(repo_path, fname):
    full_fname = os.path.join(repo_path, fname)

    return open(full_fname).read()

def get_file(repo_path, fname):
    full_fname = os.path.join(repo_path, fname)

    return open(full_fname).read()

def get_file_with_comment(repo_path, fname, comment_line, question):
    full_fname = os.path.join(repo_path, fname)

    full_src = get_file(repo_path, fname)
    lines = full_src.split("\n")

    before_comment = lines[0:comment_line] 
    comment = ["[*] [QUESTION]\t" + question]
    after_comment = lines[comment_line:]

    return "\n".join(before_comment + comment + after_comment)


def get_function_with_comment(repo_path, fname, func_start, func_end, comment_line, question):
    full_fname = os.path.join(repo_path, fname)

    full_src = get_file(repo_path, fname)
    lines = full_src.split("\n")

    before_comment = lines[func_start-1:comment_line] 
    comment = ["[*] [QUESTION]\t" + question]
    func_lines = lines[comment_line:func_end]

    return "\n".join(before_comment + comment + func_lines)

def get_function(repo_path, fname, func_start, func_end):
    full_fname = os.path.join(repo_path, fname)

    full_src = get_file(repo_path, fname)
    lines = full_src.split("\n")

    func_lines = lines[func_start-1:func_end]

    return "\n".join(func_lines)


def info_function(repo_path, sample_num, fname, func_start, func_end):
    info_validate(repo_path, sample_num)

    code = get_function(repo_path, fname, func_start, func_end)

    try:
        lexer = guess_lexer_for_filename(fname, code)
    except Exception:
        from pygments.lexers import TextLexer
        lexer = TextLexer()

    print(highlight(code, lexer, TerminalFormatter()))

def info_file(repo_path, sample_num, fname):
    info_validate(repo_path, sample_num)

    code = get_file(repo_path, fname)

    try:
        lexer = guess_lexer_for_filename(fname, code)
    except Exception:
        from pygments.lexers import TextLexer
        lexer = TextLexer()

    print(highlight(code, lexer, TerminalFormatter()))

def clone(output_dir, repo_path, repo_url, pull_id, sample_num):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(repo_path):
        run_command(["git", "clone", repo_url], cwd=output_dir)
    else:
        print(f"Repo already cloned at {repo_path}")

    run_command(["git", "fetch", "origin", f"pull/{pull_id}/head:{sample_num}"], cwd=repo_path)
    print(f"Fetched PR #{pull_id} into branch '{sample_num}'")
    


def is_checked_out(repo_path, sample_num):
    checked_out_path = os.path.join(repo_path, ".checked_out")
    if not os.path.exists(checked_out_path):
        return False
    with open(checked_out_path, "r") as f:
        stored = f.read().strip()
    return stored == str(sample_num)

def checkout_sample(repo_path, sample_num, commit):
    run_command(["git", "checkout", f"{sample_num}"], cwd=repo_path)
    print(f"checkout out {sample_num}")

    run_command(["git", "reset", "--hard", f"{commit}"], cwd=repo_path)
    print(f"Checked out SHA #{commit}'")

    checked_out_path = os.path.join(repo_path, ".checked_out")
    with open(checked_out_path, "w") as f:
        f.write(str(sample_num) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Clone repo and fetch PR")
    parser.add_argument("output_dir", help="Directory to clone into")
    parser.add_argument("sample_num", help="Sample number")
    parser.add_argument("dataset_dir", help="Sample number")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("clone", help="Clone the repo")
    subparsers.add_parser("checkout", help="Fetch pull request into local branch")

    info_parser = subparsers.add_parser("info", help="Print selected files from the repo")
    info_parser.add_argument(
        "--context",
        choices=["function", "file"],
        default="function",
        help="Specify whether to use function-level or file-level context",
        required=False
    )

    args = parser.parse_args()

    f_sample = os.path.join(args.dataset_dir, "metadata", args.sample_num + ".json")

    with open(f_sample, "r") as f:
       metadata  = json.load(f)

    repo_url = metadata["repo_url"]
    pull_id = metadata["pull_id"]
    sample_num = metadata["sample_num"]
    sha = metadata["commit"]
    fname = metadata["loc"]["file"]

    func_start = metadata["loc"]["function"]["start"]
    func_end = metadata["loc"]["function"]["end"]

    repo_name = os.path.basename(repo_url).replace(".git", "")
    repo_path = os.path.join(args.output_dir, repo_name)

    if args.command == "clone":
        clone(args.output_dir, repo_path, repo_url, pull_id, sample_num)
    elif args.command == "checkout":
        checkout_sample(repo_path, sample_num, sha)
    elif args.command == "info":
        if args.context == "function":
            info_function(repo_path, sample_num, fname, func_start, func_end)
        else:
            info_file(repo_path, sample_num, fname)

if __name__ == "__main__":
    main()

