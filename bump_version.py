import logging
import re
import subprocess
from pathlib import Path

logging.basicConfig(
    filename="version_bump.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

PYPROJECT_FILE = Path("api/pyproject.toml")
VERSION_PATTERN = r"^v?\d+\.\d+\.\d{2}$"


def validate_version(version_string):
    if not re.match(VERSION_PATTERN, version_string):

        raise ValueError(f"Invalid version format: {version_string}. " f"Expected format: v0.1.90")


def bump_version(version_string):
    validate_version(version_string)

    # Remove dev suffix, if present
    base_version = version_string.split("-")[0]

    # updated to match the 2-digit patch
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d{2})$", base_version)
    if not match:
        raise ValueError(f"Invalid version format: {version_string}")

    major_str, minor_str, patch_str = match.groups()
    major = int(major_str)
    minor = int(minor_str)
    patch = int(patch_str)

    patch += 1
    if patch > 99:
        minor += 1
        patch = 0
    if minor > 9:
        major += 1
        minor = 0

    new_version = f"v{major}.{minor}.{patch:02d}"

    return new_version


def update_version_in_pyproject(new_version):
    with open(PYPROJECT_FILE) as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.strip().startswith("version = "):
            content[i] = f'version = "{new_version}"\n'
            break
    else:
        raise ValueError("Version field not found in pyproject.toml")

    with open(PYPROJECT_FILE, "w") as file:
        file.writelines(content)


def get_current_version():
    with open(PYPROJECT_FILE) as file:
        for line in file:
            if line.strip().startswith("version = "):
                return line.split("=")[1].strip().strip('"')

    raise ValueError("Version not found in pyproject.toml")


def main():
    try:
        current_version = get_current_version()
        validate_version(current_version)
        new_version = bump_version(current_version)

        update_version_in_pyproject(new_version)

        print(f"Bumped version from {current_version} to {new_version}")

        # Stage the updated files
        subprocess.run(["git", "add", str(PYPROJECT_FILE)])

        return 0
    except ValueError as e:
        print(f"Kill yourself: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
