import importlib.resources
from pathlib import Path
from typing import Any

import pytest
import yaml


@pytest.fixture
def me_yml_data() -> Any:
    """Load the me.yml data file."""
    data_path = Path(importlib.resources.files("mypage"))  # pyright: ignore[reportArgumentType]
    me_path = data_path.parent.parent / "me.yml"
    assert me_path.exists(), "me.yml data file does not exist"
    raw_data: Any = yaml.load(me_path.read_text(), Loader=yaml.SafeLoader)  # pyright: ignore[reportAny]
    return raw_data
