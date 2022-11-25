"""Tests for GNU Compiler Collection."""


def tests_compiler():
    """Test Compiler."""
    import platform
    import subprocess
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.gcc import Compiler

    cmd = {
        "python": "",
        "--version": "",
        "-dumpversion": "",
        "not_found": False,
    }

    def dummy_compiler():
        """Force version."""
        return cmd["python"]

    def run(*popenargs, check=False, **_):
        """Mock subprocess.run."""
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
        cmd["python"] = "GCC 6.3.1 64bit"
        cmd["--version"] = "gcc (GCC) 6.3.1\n..."
        cmd["-dumpversion"] = "6.3.1"
        del compiler["python_build_version"]
        del compiler["version"]
        assert compiler.python_build_version == 6.3
        assert compiler.version == 6.3

        cmd["--version"] = "gcc (GCC) 10.2.1 20200723 (Red Hat 10.2.1-1)\n..."
        cmd["-dumpversion"] = "10"
        cmd["-dumpfullversion"] = "10.2.1"
        del compiler["version"]
        assert compiler.version == 10.2

        # Not current compiler
        assert Compiler().version == 0.0

        # Test Error
        del compiler["version"]
        cmd["not_found"] = True
        assert compiler.version == 0.0

        # Initialize system configurations
        compiler["version"] = 6.3
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


def tests_compiler_gcc_command():
    """Test Compiler if CC/GCC command available."""
    from subprocess import Popen, PIPE

    try:
        version_str = (
            Popen(["gcc", "--version"], stdout=PIPE, universal_newlines=True)
            .stdout.read()
            .lower()
        )
    except OSError:
        from pytest import skip

        version_str = ""
        skip("GCC not available")

    from compilertools.compilers.gcc import Compiler

    assert Compiler(current_compiler=True).version != 0.0 or "gcc" not in version_str
