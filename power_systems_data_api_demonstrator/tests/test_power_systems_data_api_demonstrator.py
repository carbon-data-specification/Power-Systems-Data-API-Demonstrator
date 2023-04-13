# SPDX-License-Identifier: Apache-2.0

import pytest


@pytest.mark.anyio
async def dummy_test() -> None:
    """
    Dummy test
    """
    assert True
