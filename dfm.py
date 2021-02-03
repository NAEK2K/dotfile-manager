from subprocess import check_output, CalledProcessError
import os
import json


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


def symbolic_link(target, destination):
    link_command = " ".join(
        ["ln", "-s", os.path.abspath(target), get_path(destination)]
    )
    try:
        check_output(link_command, shell=True)
    except CalledProcessError:
        pass


if __name__ == "__main__":
    starting_dir = os.getcwd()
    config = parse_json("./config.json")
    os.makedirs("dotfiles", exist_ok=True)
    clone_repo(config.get("repo_url"), "dotfiles")
    os.chdir("dotfiles")

    for directory in config.get("create_directories"):
        os.makedirs(get_path(directory), exist_ok=True)

    for dotfile in config.get("dotfiles"):
        symbolic_link(dotfile[0], dotfile[1])
