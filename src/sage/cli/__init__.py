#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys

from sage.cli.options import CliOptions


_ADVANCED_HELP = """\
SageMath command line options:

  --advanced        print this advanced help message
  --python         run the Python interpreter used by this Sage installation
  --python3        run the Python interpreter used by this Sage installation
  --sh             run a system shell with the Sage environment
  --ecl, --lisp    run the ECL Lisp interpreter
  --cleaner        run the Sage cleaner. (source-tree only)

Some source-tree developer options are unavailable in pip-installed sagelite.
In a full Sage source checkout, run the source-tree sage launcher for options
such as --root, --grep, or the Sage cleaner.
"""


def _ecl_command() -> str:
    try:
        from sagelite_ecl.runtime import ecl_command
    except ImportError:
        return "ecl"

    command = os.fspath(ecl_command())
    if os.path.isfile(command) and os.access(command, os.X_OK):
        return command
    return "ecl"


def _shell_command() -> str:
    return os.environ.get("SHELL") or "/bin/sh"


def _python_command() -> str:
    return sys.executable


def _print_advanced_help() -> int:
    print(_ADVANCED_HELP, end="")
    return 0


def main() -> int:
    input_args = sys.argv[1:]
    if input_args and input_args[0] in ("-ecl", "--ecl", "-lisp", "--lisp"):
        return subprocess.call([_ecl_command(), *input_args[1:]])
    if input_args and input_args[0] == "--sh":
        return subprocess.call([_shell_command(), *input_args[1:]])
    if input_args and input_args[0] in ("--python", "--python3"):
        return subprocess.call([_python_command(), *input_args[1:]])
    if input_args and input_args[0] == "--advanced":
        return _print_advanced_help()

    from sage.cli.eval_cmd import EvalCmd
    from sage.cli.interactive_shell_cmd import InteractiveShellCmd
    from sage.cli.notebook_cmd import JupyterNotebookCmd
    from sage.cli.run_file_cmd import RunFileCmd
    from sage.cli.version_cmd import VersionCmd

    parser = argparse.ArgumentParser(
        prog="sage",
        description="If no command is given, starts the interactive interpreter where you can enter statements and expressions, immediately execute them and see their results.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="print additional information",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="do not display the banner",
    )
    parser.add_argument(
        "--simple-prompt",
        action="store_true",
        default=False,
        help="use simple prompt IPython mode",
    )

    VersionCmd.extend_parser(parser)
    JupyterNotebookCmd.extend_parser(parser)
    EvalCmd.extend_parser(parser)
    RunFileCmd.extend_parser(parser)

    if not input_args:
        return InteractiveShellCmd(CliOptions()).run()

    args = parser.parse_args(input_args)
    options = CliOptions(**vars(args))

    logging.basicConfig(level=logging.DEBUG if options.verbose else logging.INFO)

    if args.file:
        return RunFileCmd(options).run()
    if args.command:
        return EvalCmd(options).run()
    if args.notebook:
        return JupyterNotebookCmd(options).run()
    return InteractiveShellCmd(options).run()
