"""Tests for LLVM Clang"""


def tests_compiler():
    """Test Compiler"""
    import platform
    import subprocess
    from io import StringIO
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.llvm import Compiler

    version = ""
    version_cmd = ""
    raise_error = False

    class DummyPopen:
        """Always return version in stdout"""

        def __init__(self, *_, **__):
            """Ignore arguments and raise exception on demand"""
            if raise_error:
                raise OSError

        @property
        def stdout(self):
            """Dummy stdout"""
            return StringIO(version_cmd)

    def dummy_compiler():
        """Force version"""
        return version

    platform_python_compiler = platform.python_compiler
    platform.python_compiler = dummy_compiler
    subprocess_popen = subprocess.Popen
    subprocess.Popen = DummyPopen

    try:
        compiler = Compiler(current_compiler=True)

        # Check not existing version
        assert compiler.python_build_version == 0.0
        assert compiler.version == 0.0

        # Check existing version
        version = "Clang 6.0 (clang-600.0.57)"
        version_cmd = "clang version 7.0.0 (Fedora 7.0.0-2.fc29)\n..."
        del compiler["python_build_version"]
        del compiler["version"]
        assert compiler.python_build_version == 6.0
        assert compiler.version == 7.0

        version_cmd = "Apple LLVM version 9.1.0 (clang-902.0.39.2)\n..."
        del compiler["version"]
        assert compiler.version == 9.1

        # Not current compiler
        assert Compiler().version == 0.0

        # Test Error
        del compiler["version"]
        raise_error = True
        assert compiler.version == 0.0

        # Initialize system configurations
        compiler["version"] = 7.0
        arch_x86, cpu_x86 = _get_arch_and_cpu("x86_32")
        arch_amd64, cpu_amd64 = _get_arch_and_cpu("x86_64")

        # Test API/Options
        assert len(compiler.api) > 0
        assert len(compiler.option) > 0

        # Test _compile_args_matrix
        assert compiler._compile_args_matrix(arch_x86, cpu_x86)
        assert compiler._compile_args_matrix(arch_amd64, cpu_amd64)

        # Test _compile_args_current_machine with x86
        args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
        assert args
        assert "-march=native" in args

        # Check return a result also with amd64
        assert compiler._compile_args_current_machine(arch_amd64, cpu_amd64)

        # Check -mfpmath with or without SSE
        cpu_x86["features"] = ["SSE"]
        args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
        assert "-mfpmath=sse" in args

        cpu_x86["features"] = []
        args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
        assert "-mfpmath=sse" not in args

    finally:
        platform.python_compiler = platform_python_compiler
        subprocess.Popen = subprocess_popen


def tests_compiler_clang_command():
    """Test Compiler if CC/Clang command available"""
    from subprocess import Popen, PIPE

    try:
        version_str = (
            Popen(["clang", "--version"], stdout=PIPE, universal_newlines=True)
            .stdout.read()
            .lower()
        )
    except OSError:
        from pytest import skip

        version_str = ""
        skip("Clang not available")

    from compilertools.compilers.llvm import Compiler

    assert Compiler(current_compiler=True).version != 0.0 or "clang" not in version_str
