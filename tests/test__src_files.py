"""Tests for source file parsing utilities"""


def tests_any_line_startswith():
    """"Test _any_line_startswith"""
    from tempfile import TemporaryDirectory
    from os.path import join
    from compilertools._src_files import _any_line_startswith

    with TemporaryDirectory() as tmp:
        # Create dummy files
        files = [join(tmp, "file.ext1"), join(tmp, "file.ext2")]
        with open(files[0], "wt") as file:
            file.write("\nazerty\n\tuiop\nqsdfgh\n")
        with open(files[1], "wt") as file:
            file.write("\tWXCVBN\nUIOP\n   JKLM\n")

        # Test existing files content
        assert _any_line_startswith(files, {".ext1": "uiop"})

        # Test ignore case
        assert _any_line_startswith(files, {".ext2": "uiop"})

        # Test non existing file
        assert not _any_line_startswith(files, {".ext3": "uiop"})

        # Test non existing file content
        assert not _any_line_startswith(files, {".ext1": "wxcvbn", ".ext2": "azerty"})

        # Test content list
        assert _any_line_startswith(files, {".ext1": ["uiop", "qsd"]})

        # Test str argument auto-conversion
        assert _any_line_startswith(files[0], {".ext1": "uiop"})


def tests_ignore_api():
    """Test _ignore_api"""
    from compilertools.compilers import CompilerBase
    from compilertools._src_files import _ignore_api

    # Create compiler
    compiler = CompilerBase()

    # No compiler
    assert _ignore_api(None, "test") is False

    # API not supported
    assert _ignore_api(compiler, "test") is True

    # API supported (compiler)
    compiler["api"]["test"] = {}
    assert _ignore_api(compiler, "test") is False


def tests_startwith_exts():
    """Test _startswith_exts"""
    from compilertools._src_files import _startswith_exts

    # List arguments
    result = _startswith_exts(
        c=["c1", "c2"], fortran=["fortran"], not_exists=["not_exists"]
    )
    assert list(result[".c"]) == ["c1", "c2"]
    assert list(result[".f"]) == ["fortran"]
    assert [key for key in result if "not_exists" in result[key]] == []

    # str or None arguments
    result = _startswith_exts(c="c", fortran=None)
    assert result[".c"] == ("c",)
    assert ".f" not in result


def tests_use_api_pragma():
    """Test _use_api_pragma"""
    from tempfile import TemporaryDirectory
    from os.path import join
    from compilertools.compilers import CompilerBase
    from compilertools._src_files import _use_api_pragma

    compiler = CompilerBase()

    with TemporaryDirectory() as tmp:
        files = [join(tmp, "file.c"), join(tmp, "file.ext2")]
        with open(files[0], "wt") as file:
            file.write("\nazerty\n\tuiop\nqsdfgh\n")
        with open(files[1], "wt") as file:
            file.write("\tytreza\n\tuiop\nqsdfgh\n")

        # API not supported by compiler
        assert _use_api_pragma(files, compiler, "test", c="azerty") is False

        # API supported and file using it
        compiler["api"]["test"] = {}
        assert _use_api_pragma(files, compiler, "test", c="azerty") is True

        # API suppoted but file not using it
        assert _use_api_pragma(files, compiler, "test", c="ytreza") is False
