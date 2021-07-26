#!/usr/bin/env python
import argparse
import os
import sys
import webbrowser

from datetime import datetime
from statistics import median
from subprocess import (
    call,
    check_call,
    check_output,
    CalledProcessError,
    DEVNULL,
    STDOUT,
)

import nbformat
import requests

from nbconvert.preprocessors import ExecutePreprocessor


def fetch_count(username, token, samples=5):
    """Queries the GitHub API to get the current ipynb count.

    Takes the median of multiple samples and truncates to an int.

    Parameters
    ----------
    username: str
        GitHub API username
    token: str
        GitHub API token
    samples: int
        Number of samples to take from the GitHub API

    Returns
    -------
    int
    """
    counts = []
    for i in range(samples):
        resp = requests.get(
            "https://api.github.com/search/code?q=nbformat+in:file+extension:ipynb",
            headers={"Accept": "application/vnd.github.v3+json"},
            auth=(username, token),
        )
        resp.raise_for_status()
        counts.append(resp.json()["total_count"])
    return int(median(counts))


def store_count(date, count, filename="ipynb_counts.csv"):
    """Reads the CSV containing the historical `year-month-day,count` pairs
    and upserts the count for the current date.

    Parameters
    ----------
    date: str
        Date in year-month-day format
    count: int
        Count of ipynb files
    filename: str
        CSV filename
    """
    # Read the historical counts if the file containing them exists
    if os.path.isfile(filename):
        with open(filename) as fh:
            lines = fh.readlines()
        counts = dict(line.strip().split(",") for line in lines[1:])
    else:
        counts = {}

    # Upsert the count for the given date
    counts[date] = count

    # Write out the CSV sorted by date
    with open(filename, "w") as fh:
        fh.write("date,hits\n")
        for date in sorted(counts):
            fh.write(f"{date},{counts[date]}\n")


def execute_notebook(src="estimate.src.ipynb", dest="estimate.ipynb"):
    """Executes the analysis notebook and writes out a copy with all of the
    resulting tables and plots.

    Parameters
    ----------
    src: str, optional
        Source notebook to execute
    dest: str, optional
        Output notebook
    """
    with open(src) as fp:
        nb = nbformat.read(fp, 4)

    exp = ExecutePreprocessor(timeout=300)
    updated_nb, _ = exp.preprocess(nb, {})

    with open(dest, "w") as fp:
        nbformat.write(updated_nb, fp)


def configure_ci_git(token, repo="parente/nbestimate"):
    """Configures CI to push to GitHub.

    Parameters
    ----------
    token: str
        GitHub API token
    repo: str, optional
        GitHub org/repo
    """
    call(["git", "remote", "rm", "origin"])
    check_call(
        ["git", "remote", "add", "origin", f"https://{token}@github.com/{repo}.git"],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )
    call(["git", "config", "--global", "user.name", "GitHub Actions"])
    call(
        ["git", "config", "--global", "user.email", "actions@users.noreply.github.com"]
    )


def git_commit_and_push(date):
    """Commits all changed files in the local sandbox and pushes them to origin-pushback.

    Parameters
    ----------
    date: str
        Date in year-month-day format
    """
    print(check_output(["git", "checkout", "master"], encoding="utf-8"))
    print(
        check_output(
            ["git", "commit", "-a", "-m", "Update for {}".format(date)],
            encoding="utf-8",
        )
    )
    print(check_output(["git", "push", "origin", "master"], encoding="utf-8"))


def main(argv):
    """Uses the GitHub API to estimate the current count of public ipynb files on GitHub,
    stores that count in a CSV file associated with today's date (localtime), executes
    a notebook to analyze the growth, and commits the CSV and executed notebook back
    to GitHub.

    Parameters
    ----------
    argv: list
        Command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assert-more-than",
        type=int,
        default=0,
        help="Abort further actions if the count is less than the given value",
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip fetching the current count from GitHub",
    )
    parser.add_argument(
        "--skip-execute",
        action="store_true",
        help="Skip executing the notebook analysis",
    )
    parser.add_argument(
        "--skip-push",
        action="store_true",
        help="Skip committing and pushing the result to GitHub",
    )
    args = parser.parse_args(argv)

    date = datetime.now().strftime("%Y-%m-%d")

    if not args.skip_fetch:
        print(f"Fetching count for {date}")
        count = fetch_count("parente", os.environ["GITHUB_TOKEN"])
        assert count >= args.assert_more_than, f"{count} < {args.assert_more_than}"
        print(f"Storing count {count} for {date}")
        store_count(date, count)

    if not args.skip_execute:
        print("Executing notebook")
        execute_notebook()

    if not args.skip_push:
        if os.getenv("CI"):
            print("Configuring CI for commit to GitHub")
            configure_ci_git(os.environ["GITHUB_TOKEN"])
        print("Conmitting and pushing update")
        git_commit_and_push(date)


if __name__ == "__main__":
    main(sys.argv[1:])
