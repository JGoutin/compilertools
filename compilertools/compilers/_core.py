# -*- coding: utf-8 -*-
"""Base class and functions for compilers"""
from itertools import product
from collections import namedtuple, OrderedDict
from compilertools._utils import import_class, BaseClass
from compilertools.processors import get_processor, get_arch

__all__ = ['CompilerBase', 'get_compiler']


def get_compiler(compiler=None):
    """Return compiler class

    compiler: Compiler Name or instance"""
    # Return compiler instance
    if isinstance(compiler, CompilerBase):
        return compiler

    # Use distutils default compiler as default
    if compiler is None:
        from distutils.ccompiler import get_default_compiler
        compiler = get_default_compiler()

    # Aliases for compilers names
    if compiler in ('mingw32', 'cygwin'):
        compiler = 'gcc'

    # Return compiler
    return import_class('compilers', compiler, 'Compiler', CompilerBase)()


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

       build_if: Condition that must be True for cimpile file with
           this argument and the current compiler (Ex compiler version).
           Default value is True.""")

    def get_arch_and_cpu(self, arch=None, current_machine=False):
        """Return arch and update CPU linked to compiler

        arch: if None, use current computer arch, else use specified"""
        # Get Architecture
        arch = get_arch(arch)

        # Get CPU
        self._cpu = get_processor(arch, current_machine=current_machine)
        return get_arch(arch)

    def compile_args(self, arch=None, current_machine=False,
                     current_compiler=False):
        """Get compiler args list for a specific architecture.

        arch : target architecture name.
        current_machine : If True, return only arguments compatibles with
            current machine (conditions from "import_if").
        current_compiler : If True, return only arguments compatibles with
            current compiler (conditions from "build_if")."""
        # Update arch and CPU
        arch = self.get_arch_and_cpu(arch, current_machine=current_machine)

        # Compute argments
        return self._order_args_matrix(self.compile_args_matrix(arch),
                                       current_machine, current_compiler)

    def compile_args_matrix(self, arch):  # @UnusedVariable
        """Return compiler arguments availables for the specified CPU
        architecture as a matrix.

        arch: CPU Architecture str."""
        return []

    def compile_args_current_machine(self):
        """Return compiler arguments optimised by compiler for current
        machine"""
        # Update arch and CPU
        arch = self.get_arch_and_cpu(current_machine=True)

        # Compute argments
        args = self.compile_args(arch, current_machine=True)
        return args[args.keys()[0]]

    @staticmethod
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

    @property
    def version(self):
        """Compiler version"""
        return self._get_attr('version', 0.0)

    def support_api(self, api):
        """Check if compiler support specific API.

        api: API name ('openmp', 'openacc', 'cilkplus')"""
        if ('%s_compile' % api in self._attributes or
                '%s_link' % api in self._attributes):
            return True
        return False

    @property
    def openmp_compile_arg(self):
        """Compiler argument for openMP"""
        return self._get_attr('openmp_compile', '')

    @property
    def openmp_link_arg(self):
        """Linker argument for openMP"""
        return self._get_attr('openmp_link', '')

    @property
    def openacc_compile_arg(self):
        """Compiler argument for OpenACC"""
        return self._get_attr('openacc_compile', '')

    @property
    def openacc_link_arg(self):
        """Linker argument for OpenACC"""
        return self._get_attr('openacc_link', '')

    @property
    def cilkplus_compile_arg(self):
        """Compiler argument for Intel® Cilk™ Plus"""
        return self._get_attr('cilkplus_compile', '')

    @property
    def cilkplus_link_arg(self):
        """Linker argument for Intel® Cilk™ Plus"""
        return self._get_attr('cilkplus_link', '')

    @property
    def fast_fpmath_compile_arg(self):
        """Compiler argument for Fast floating point calculations"""
        return self._get_attr('fast_fpmath', '')
