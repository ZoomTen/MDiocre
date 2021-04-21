# Based on code by: Douglas Creager <dcreager@dcreager.net>

__all__ = ("get_git_version")

from subprocess import Popen, PIPE
import re

def git2pep440(git_ver):
    """Transforms git-describe output into PEP440 compatible format.

    Examples:
        v1.0.1.rc5-24-abcdef => 1.0.1.rc5+24.abcdef
        v3.0-90-a89abc => 3.0+90.a89abc
    """
    def _git2pep440(match):
        major, minor, _3, patch, _5, rcdevversion, rcdevtype,_8, distance, _10, \
        commit = match.groups()
        version_string = f"{major}.{minor}"
        if _3:
            version_string += f".{patch}"
        if _5:
            version_string += f".{rcdevversion}"
        if _8:
            version_string += f"+{distance}.{commit}"
        return version_string
    
    return re.sub('v?([0-9]+)\.([0-9]+)(\.([0-9]+))?(\.((rc|dev)[0-9]+))?(-([0-9]+))?(-g([0-9a-fA-F]+))?', _git2pep440, git_ver)


def call_git_describe(abbrev):
    """Queries git-describe for the git version number, then returns a PEP440
    compatible version string.
    """
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0].strip().decode('ascii')
        return git2pep440(line)
    except:
        return None


def is_dirty():
    """Checks if the working tree is currently dirty."""
    try:
        p = Popen(["git", "diff-index", "--name-only", "HEAD"],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        lines = p.stdout.readlines()
        return len(lines) > 0
    except:
        return False


def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()
    except:
        return None


def write_release_version(version):
    with open("RELEASE-VERSION", "w") as f:
        f.write(f"{version}\n")

def get_git_version(abbrev=7):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()

    # First try to get the current version using “git describe”.

    version = call_git_describe(abbrev)
    if is_dirty():
        version += ".dirty"

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        write_release_version(version)

    # Finally, return the current version.
    return version


if __name__ == "__main__":
    print(get_git_version())
