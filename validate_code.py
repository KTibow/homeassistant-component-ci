import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    startgroup("Hassfest")
    repo_name = os.getenv("GITHUB_REPOSITORY").split("/")[1].lower()
    os.system(
        """docker run --name hassfest_instance --workdir /github/workspace --rm """
        + f"""-v "/home/runner/work/{repo_name}/{repo_name}":"/github/workspace" hassfest"""
    )
    endgroup()
    errors = os.system("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics")
    if errors != 0:
        raise Exception("Python is invalid, according to flake8")
    startgroup("Flake8: Unused stuff and docstrings")
    flake8start = """flake8 . --inline-quotes '"' --count --exit-zero --max-complexity=15 --max-line-length=90 --statistics """
    os.system(flake8start + "--select=D,DAR")
    os.system(flake8start + "--select=F")
    endgroup()
    startgroup("Flake8: Other random stuff")
    os.system(flake8start + "--select=I,P,WPS305,C812,E203,W503,E800")
    os.system(flake8start + "--ignore=I,P,WPS305,C812,E203,W503,E800,D,DAR,F")
    endgroup()
else:
    print("No python files found, not running hassfest and flake8.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("ESLint")
    if ".eslintrc" in "".join(glob.glob("**/*", recursive=True)):
        print("Eslint already exists, not changing.")
    else:
        shutil.copyfile(
            "/home/runner/work/_actions/KTibow/ha-blueprint/main/.eslintrc.js",
            ".eslintrc.js",
        )
    os.system("npx eslint . -f summary --quiet --ext js,ts")
    endgroup()
else:
    print("No JS files found, not running eslint.")
