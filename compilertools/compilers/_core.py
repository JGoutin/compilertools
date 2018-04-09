# -*- coding: utf-8 -*-
"""Base class and functions for compilers"""
from itertools import product
from collections import namedtuple, OrderedDict
from compilertools._utils import import_class, BaseClass
from compilertools._config import CONFIG
from compilertools.processors import get_processor, get_arch

__all__ = ['CompilerBase', 'get_compiler']


def get_compiler(compiler=None, current_compiler=False):
    """Return compiler class

    compiler: Compiler Name or instance
    current_compiler: Compiler used to build"""
    # Return compiler instance
    if isinstance(compiler, CompilerBase):
        return compiler

    # Use distutils default compiler as default
    if compiler is None:
        from distutils.ccompiler import get_default_compiler
        compiler = get_default_compiler()

    # Aliases for compilers names
    compiler = CONFIG.get('compilers', {}).get(compiler, compiler)

    # Return compiler
    return import_class('compilers', compiler, 'Compiler', CompilerBase)(
        current_compiler=current_compiler)


def _get_arch_and_cpu(arch=None, current_machine=False):
    """Return arch and update CPU linked to compiler

    arch: if None, use current computer arch, else use specified"""
    # Get Architecture
    arch = get_arch(arch)

    # Get CPU
    return arch, get_processor(arch, current_machine=current_machine)


def _order_args_matrix(args_matrix, current_machine=False,
                       current_compiler=False):
    """Convert args matrix to args ordered dict {suffix: arg}

    args_matrix : result from self._compile_args_matrix or
        self._link_args_matrix
    current_machine : If True, return only arguments compatibles with
        current machine (conditions from "import_if").
    current_compiler : If True, return only arguments compatibles with
        current compiler (conditions from "build_if")."""

    # Create args combinations from args matrix
    args_combinations = OrderedDict()
    for args in product(*args_matrix):
        args_list = []
        suffix_list = []
        is_compatible = True
        for arg in args:
            # Import conditions
            if current_machine:
                is_compatible = not(
                    not arg.import_if or not is_compatible)

            # Build condition
            if current_compiler:
                is_compatible = not(
                    not arg.build_if or not is_compatible)

            # Don't add incompatible args
            if not is_compatible:
                break

            # Get argument
            arg_arg = arg.args
            if arg_arg:
                if isinstance(arg_arg, str):
                    args_list.append(arg_arg)
                else:
                    args_list.extend(arg_arg)

            # Get suffix
            arg_suffix = arg.suffix
            if arg_suffix:
                suffix_list.append(arg_suffix.
                                   replace('.', '_').
                                   replace('-', '_'))

        # Add compatibles args
        if is_compatible:
            args_combinations['-'.join(suffix_list)] = args_list

    return args_combinations


class CompilerBase(BaseClass):
    """Base class for compiler"""

    # Argument class
    Arg = namedtuple('Argument', 'args suffix import_if build_if')
    Arg.__new__.__defaults__ = ('', '', True, True)
    Arg.__doc__ = ("""
       Compiler argument.

       args: arguments sent to compiler (ex "-flto -w").

       suffix: suffix related to this argument in compiled file name.

       import_if: condition that must be True for importing file
           compiled with this argument (ex architecture compatibility).
           Default value is True.

       build_if: Condition that must be True for compile file with
           this argument and the current compiler (Ex compiler version).
           Default value is True.""")

    def __init__(self, current_compiler=False):
        BaseClass.__init__(self)
        self['current_compiler'] = current_compiler
        self._default['current_compiler'] = False
        self._default['version'] = 0.0

    def _compile_args_matrix(self, arch, cpu):
        """Return available compiler arguments for the specified CPU
        architecture as a matrix.

        Override for define matrix.

        arch: CPU Architecture str.
        cpu: Processor instance"""
        raise NotImplementedError

    def _compile_args_current_machine(self, arch, cpu):
        """Define optimized arguments for current machine.

        By default, get the best options from compile_args method.

        Override for define another behavior.

        arch: CPU Architecture str
        cpu: Processor instance"""
        args = _order_args_matrix(
            self._compile_args_matrix(arch, cpu), current_machine=True)

        if not args:
            return []
        return args[list(args)[0]]

    def compile_args(self, arch=None, current_machine=False):
        """Get compiler args list for a specific architecture.

        arch : target architecture name.
        current_machine : If True, return only arguments compatibles with
            current machine (conditions from "import_if")."""
        return _order_args_matrix(
            self._compile_args_matrix(
                *_get_arch_and_cpu(arch, current_machine=current_machine)),
            current_machine, self['current_compiler'])

    def compile_args_current_machine(self):
        """Return compiler arguments optimized by compiler for current
        machine"""
        return self._compile_args_current_machine(
            *_get_arch_and_cpu(current_machine=True))

    @BaseClass._memoized_property
    def name(self):
        """Compiler type name"""
        return self.__module__.rsplit('.', 1)[-1]

    @BaseClass._memoized_property
    def api(self):
        """Compatibles API"""
        return {}

    @BaseClass._memoized_property
    def option(self):
        """Compatibles Options"""
        return {}
