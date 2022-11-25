"""Test for general configuration."""


def tests_config():
    """Test CONFIG."""
    from collections.abc import Mapping
    from compilertools._config import CONFIG

    # Check sections presence and type
    assert isinstance(CONFIG.get("architectures"), Mapping)
    assert isinstance(CONFIG.get("compilers"), Mapping)
