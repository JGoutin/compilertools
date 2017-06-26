# -*- coding: utf-8 -*-
"""Tests for source file parsing utilities"""
from tempfile import TemporaryDirectory
from os.path import join
from compilertools._src_files import _any_line_startwith


def tests_any_line_startwith():
    """"Test _any_line_startwith"""
    with TemporaryDirectory() as tmp:
        # Create file
        files = [join(tmp, 'file.ext1'), join(tmp, 'file.ext2')]
        with open(files[0], 'wt') as file:
            file.write("\nazerty\n\tuiop\nqsdfgh\n")
        with open(files[1], 'wt') as file:
            file.write("\tWXCVBN\nUIOP\n   JKLM\n")

        # Test files content
        assert _any_line_startwith(files, {
            '.ext1': 'uiop'})
        assert _any_line_startwith(files, {
            '.ext2': 'uiop'})
        assert not _any_line_startwith(files, {
            '.ext3': 'uiop'})
        assert not _any_line_startwith(files, {
            '.ext1': 'wxcvbn', '.ext2': 'azerty'})
