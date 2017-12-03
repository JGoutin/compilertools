# -*- coding: utf-8 -*-
"""Test for build configuration"""

def tests_config_build():
    """Test CONFIG_BUILD"""
    from collections.abc import Mapping
    from compilertools._config_build import CONFIG_BUILD

    # Check sections presence and type
    assert isinstance(CONFIG_BUILD.get('option'), Mapping)
    assert isinstance(CONFIG_BUILD.get('api'), Mapping)
    assert isinstance(CONFIG_BUILD.get('extensions'), Mapping)
