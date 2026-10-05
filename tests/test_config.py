from pathlib import Path

import pytest

from raven.core.config import load_config


def test_example_config_is_authorized_and_mock_only() -> None:
    config = load_config(Path("configs/example.yaml"))
    assert config.authorization.confirmed is True
    assert config.target.adapter == "mock"
    assert config.safety.allowed_targets == ["mock"]


def test_config_rejects_missing_authorization(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        "authorization:\n  confirmed: false\n  scope_reference: local\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="authorization.confirmed"):
        load_config(path)
