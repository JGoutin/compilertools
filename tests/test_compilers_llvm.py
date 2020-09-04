"""Tests for LLVM Clang"""


def tests_compiler():
    """Test Compiler"""
    import platform
    import subprocess
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.llvm import Compiler

    cmd = {
        "python": "",
        "--version": "",
        "-dumpversion": "",
        "not_found": False,
    }

    def dummy_compiler():
        """Force version"""
        return cmd["python"]

    def run(*popenargs, check=False, **_):
        """Mocked subprocess.run"""
        args = popenargs[0]
        if cmd["not_found"]:
            raise FileNotFoundError
        try:
            stdout = cmd[args[1]]
            return_code = 0
        except KeyError:
            stdout = ""
            return_code = 1
            if check:
                raise subprocess.CalledProcessError(return_code, args)
        return subprocess.CompletedProcess(args, return_code, stdout)

    platform_python_compiler = platform.python_compiler
    platform.python_compiler = dummy_compiler
    subprocess_run = subprocess.run
    subprocess.run = run

    try:
        compiler = Compiler(current_compiler=True)

        # Check not existing version
        assert compiler.python_build_version == 0.0
        assert compiler.version == 0.0

        # Check existing version
        cmd["python"] = "Clang 6.0 (clang-600.0.57)"
        cmd["--version"] = "clang version 7.0.0 (Fedora 7.0.0-2.fc29)\n..."
        cmd["-dumpversion"] = "7.0.0"
        del compiler["python_build_version"]
        del compiler["version"]
        assert compiler.python_build_version == 6.0
        assert compiler.version == 7.0

        cmd["--version"] = "Apple LLVM version 9.1.0 (clang-902.0.39.2)\n..."
        cmd["-dumpversion"] = "9.1.0"
        del compiler["version"]
        assert compiler.version == 9.1

        # Not current compiler
        assert Compiler().version == 0.0

        # Test Error
        del compiler["version"]
        cmd["not_found"] = True
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
        subprocess.run = subprocess_run


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
