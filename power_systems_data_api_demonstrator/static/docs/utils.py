# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

base_path = Path(__file__).parent


def get_app_title() -> str:
    """
    Get the app title from the pyproject.toml file.

    :return: app title.
    """
    with open(base_path / "title.txt") as f:
        title = f.read()
    return title


def get_app_description() -> str:
    """
    Get the app description from the pyproject.toml file.

    :return: app description.
    """
    with open(base_path / "description.md") as f:
        description = f.read()
    return description
