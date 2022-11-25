"""Test for build configuration."""


def tests_config_build():
    """Test CONFIG_BUILD."""
    from collections.abc import Mapping, Container
    from compilertools._config_build import ConfigBuild

    # Check sections presence and type
    assert isinstance(ConfigBuild.option, Mapping)
    assert isinstance(ConfigBuild.api, Mapping)
    assert isinstance(ConfigBuild.extensions, Mapping)
    assert isinstance(ConfigBuild.suffixes_includes, Container)
    assert isinstance(ConfigBuild.suffixes_excludes, Container)
