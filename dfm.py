#!/bin/python3

from subprocess import check_output, CalledProcessError
import os
import json
import argparse
import shutil


def parse_json(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def clone_repo(repo_url, directory):
    git_command = " ".join(["git", "clone", repo_url, directory])
    try:
        check_output(git_command, shell=True)
    except CalledProcessError:
        pass


def get_path(path):
    return os.path.expandvars(os.path.expanduser(path))


def create_symbolic_link(target, destination):
    link_command = " ".join(
        ["ln", "-s", os.path.abspath(target), get_path(destination)]
    )
    try:
        check_output(link_command, shell=True)
    except CalledProcessError:
        pass


def remove_symbolic_link(link_path):
    os.unlink(link_path)


def update_repo():
    git_command = " ".join(["git", "fetch;", "git", "pull", "--force"])
    try:
        check_output(git_command, shell=True)
    except CalledProcessError:
        pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--remake", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    config = parse_json("./config.json")

    if args.clean:
        shutil.rmtree("./dotfiles")

    os.makedirs("dotfiles", exist_ok=True)
    clone_repo(config.get("repo_url"), "dotfiles")
    os.chdir("dotfiles")

    if args.update:
        update_repo()

    for directory in config.get("create_directories"):
        os.makedirs(get_path(directory), exist_ok=True)

    if args.remake:
        for dotfile in config.get("dotfiles"):
            remove_symbolic_link(get_path(dotfile[1]))

    for dotfile in config.get("dotfiles"):
        create_symbolic_link(get_path(dotfile[0]), get_path(dotfile[1]))
