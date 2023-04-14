# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import yaml


def load_grid_nodes():
    config_file = Path(__file__).parent / "grid_nodes.yaml"
    with open(config_file, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config["nodes"]


GRID_NODES = load_grid_nodes()
