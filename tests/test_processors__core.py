# -*- coding: utf-8 -*-
"""Tests for processors core"""

def tests_get_arch():
    """Test get_arch"""
    from platform import machine
    from compilertools._config import CONFIG
    from compilertools.processors._core import get_arch

    # Test lower case
    assert get_arch('ARCH') == 'arch'

    # Current arch
    arch = machine().lower()
    assert get_arch() == CONFIG['architectures'].get(arch, arch)

    # Test aliases
    for arch in CONFIG['architectures']:
        assert get_arch(arch) == CONFIG['architectures'][arch]

    # Test cross compilation
    assert get_arch('x86_amd64') == 'x86_64'

    # Test prefixed architecture
    assert get_arch('linux-x86_64') == 'x86_64'


def tests_get_processor():
    """Test get_processor"""
    from os import listdir
    from os.path import splitext, dirname
    from compilertools.processors import _core
    from compilertools.processors._core import get_processor
    from itertools import product

    # Return processor by name
    # with all file in "compilertools.processors"
    for file, current_machine in product(listdir(dirname(_core.__file__)),
                                         (True, False)):
        if file.startswith('_'):
            continue
        name = splitext(file)[0]

        processor = get_processor(name, current_machine=current_machine)
        assert (processor.__class__.__module__ ==
                'compilertools.processors.%s' % name)
        assert processor.current_machine is current_machine


def tests_processor_base():
    """Test ProcessorBase"""
    from compilertools.processors import ProcessorBase

    # Test current machine
    processor = ProcessorBase()
    assert processor.current_machine is False

    processor = ProcessorBase(current_machine=True)
    assert processor.current_machine is True

    # Test properties
    assert processor.vendor == ''
    processor['vendor'] = 'vendor'
    assert processor.vendor == 'vendor'

    assert processor.brand == ''
    processor['brand'] = 'brand'
    assert processor.brand == 'brand'

    assert processor.features == []
    processor['features'] = ['feature1', 'feature2']
    assert processor.features == ['feature1', 'feature2']

    # Test arch
    assert processor.arch == '_core'
