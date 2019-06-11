#!/usr/bin/env python
import subprocess
import sys


VERSION = "0.2.0"


def main():
    args = sys.argv[1:]
    if args and args[0] == "version":
        print(f"git-branchstat {VERSION}")
        sys.exit(1)
    if not is_git_repo():
        print("Not a git repo.")
        sys.exit(1)
    outputs = [get_ahead_behind(), get_modified(), get_status(), get_untracked()]
    valid = [o for o in outputs if o]
    print(", ".join(valid))


def get_ahead_behind():
    # out, err := git_output("for-each-ref", "--format='%(refname:short) %(upstream:track)'", "refs/heads")
    # if err != nil :
    #     log.Fatalf("%s\n", err)

    # changedBranches := []string{}
    # for _, line := range strings.Split(out, "\n") :
    #     tidied := strings.Trim(line, "'\" ")
    #     if len(strings.Split(tidied, " ")) > 1 :
    #         changedBranches = append(changedBranches, tidied)


    # return strings.Join(changedBranches, ", ")
    raise Exception("Not implemented!")


def get_modified():
    # out, err := git_output([]string{"diff", "--stat"})
    # if err != nil :
    #     log.Fatal(err)

    # nmodified := strings.Count(strings.TrimRight(out, "\n"), "\n")
    # msg := ""
    # if nmodified > 0 :
    #     msg = fmt.Sprintf("Modified %d", nmodified)

    raise Exception("Not implemented!")


def get_status():
    # out, err := git_output([]string{"diff", "--stat", "--cached"})
    # if err != nil :
    #     log.Fatal(err)

    # nstaged := strings.Count(out, "\n")
    # msg := ""
    # if nstaged > 0 :
    #     msg = fmt.Sprintf("Staged %d", nstaged)

    raise Exception("Not implemented!")


def get_untracked():
    # out, err := git_output([]string{"ls-files", "--others", "--exclude-standard"})
    # if err != nil :
    #     log.Fatal(err)

    # nuntracked := strings.Count(out, "\n")
    # msg := ""
    # if nuntracked > 0 :
    #     msg = fmt.Sprintf("Untracked %d", nuntracked)

    raise Exception("Not implemented!")


def git_output(*args):
    finished = subprocess.run(["git", *args])
    print(finished.returncode == 128)
    # cmdEditor := exec.Command("git", args...)
    # out, err := cmdEditor.Output()
    # if err != nil :
    #     return "", err

    # return string(out[:]), nil
    raise Exception("Not implemented!")


def is_git_repo():
    finished = subprocess.run(["git", "branch"], capture_output=True)
    return finished.returncode != 128


if __name__ == "__main__":
    main()
