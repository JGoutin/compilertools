# -*- coding: utf-8 -*-
"""Test for general configuration"""

def tests_config():
    """Test CONFIG"""
    from collections.abc import Mapping
    from compilertools._config import CONFIG

    # Check sections presence and type
    assert isinstance(CONFIG.get('arch_alias'), Mapping)
    assert isinstance(CONFIG.get('compiler_alias'), Mapping)
