#!/usr/bin/env python3
"""Sync the latest stable OpenInvento release into this Home Assistant app."""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config.yaml"
CHANGELOG = ROOT / "CHANGELOG.md"
RELEASES_API = "https://api.github.com/repos/openinvento/openinvento/releases/latest"
RELEASES_URL = "https://github.com/openinvento/openinvento/releases/tag/"


def write_output(name: str, value: str) -> None:
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"{name}={value}\n")


def version_tuple(version: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError(f"Expected a stable semantic version, got {version!r}")
    return tuple(int(part) for part in version.split("."))  # type: ignore[return-value]


def latest_release() -> tuple[str, str]:
    request = urllib.request.Request(
        RELEASES_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "openinvento-home-assistant-release-sync",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)

    tag = release["tag_name"]
    version = tag.removeprefix("v")
    version_tuple(version)
    return version, tag


def main() -> None:
    config_text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r"(?m)^version:\s*[\"']?([0-9.]+)[\"']?\s*$", config_text)
    if not match:
        raise RuntimeError("Could not read the app version from config.yaml")

    current_version = match.group(1)
    upstream_version, upstream_tag = latest_release()
    write_output("upstream_tag", upstream_tag)

    if version_tuple(upstream_version) <= version_tuple(current_version):
        write_output("changed", "false")
        write_output("version", current_version)
        return

    updated_config = config_text[: match.start()] + f'version: "{upstream_version}"' + config_text[match.end() :]
    CONFIG.write_text(updated_config, encoding="utf-8", newline="\n")

    changelog_text = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# Changelog\n"
    if not changelog_text.startswith("# Changelog"):
        changelog_text = "# Changelog\n\n" + changelog_text.lstrip()
    release_link = RELEASES_URL + urllib.parse.quote(upstream_tag, safe="")
    entry = (
        f"## {upstream_version}\n\n"
        f"- OpenInvento release: [{upstream_tag}]({release_link})\n\n"
    )
    changelog_text = changelog_text.replace("# Changelog\n", "# Changelog\n\n" + entry, 1)
    CHANGELOG.write_text(changelog_text, encoding="utf-8", newline="\n")

    write_output("changed", "true")
    write_output("version", upstream_version)


if __name__ == "__main__":
    main()
