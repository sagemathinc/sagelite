#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys

from sage.cli.options import CliOptions


def _ecl_command() -> str:
    try:
        from sagelite_ecl.runtime import ecl_command
    except ImportError:
        return "ecl"

    command = os.fspath(ecl_command())
    if os.path.isfile(command) and os.access(command, os.X_OK):
        return command
    return "ecl"


def main() -> int:
    input_args = sys.argv[1:]
    if input_args and input_args[0] in ("-ecl", "--ecl", "-lisp", "--lisp"):
        return subprocess.call([_ecl_command(), *input_args[1:]])

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
