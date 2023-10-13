# Copyright 2019-2020 Faculty Science Limited
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import sys
from pathlib import Path
from argparse import ArgumentParser

from termcolor import colored


LICENSE_HEADER = """
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
LICENSE_HEADER_LINES = LICENSE_HEADER.strip().split("\n")


def python_files(path, include_hidden, excludes):
    if not include_hidden and path.match(".*"):
        # Path is hidden, ignore:
        return
    elif path in excludes:
        return
    elif path.is_dir():
        for child in path.iterdir():
            yield from python_files(child, include_hidden, excludes)
    elif path.is_file() and path.suffix == ".py":
        yield path


def is_empty(path):
    content = path.read_text()
    return len(content.strip()) == 0


def read_header_lines(path):

    header_lines = []

    with path.open() as fp:

        for line in fp.readlines():

            stripped_line = line.strip()

            # Ignore empty lines
            if stripped_line == "":
                continue

            # Stop when non-comment line reached
            if not stripped_line.startswith("#"):
                break

            header_lines.append(stripped_line)

    return header_lines


def check_license(lines):
    return all(line in lines for line in LICENSE_HEADER_LINES)


def check_copyright(lines, copyright):
    for line in lines:
        if line.startswith("# Copyright"):
            return copyright in line
    else:
        # No copyright line found
        return False


def format_success(success):
    if success:
        return colored("YES", "green")
    else:
        return colored("NO", "red")


def cli():
    parser = ArgumentParser(
        description="Check Python source files for Apache License headers"
    )
    parser.add_argument(
        "path",
        nargs="*",
        type=Path,
        default=[Path.cwd()],
        help="path(s) of files or directories to check",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="also check hidden files and directories",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="require empty files (e.g. empty __init__.py), which are skipped "
        + "by default",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        type=Path,
        default=[],
        help="path(s) of files or directories to ignore",
    )
    parser.add_argument(
        "--copyright",
        help="check that the header has a copyright notice containing the "
        + "provided substring",
    )
    args = parser.parse_args()

    success = True

    for passed_path in args.path:
        for file in python_files(
            passed_path, args.include_hidden, args.exclude
        ):

            output = str(file)

            if not args.include_empty and is_empty(file):
                output += " " + colored("EMPTY", "yellow")
            else:
                header_lines = read_header_lines(file)

                if args.copyright is not None:
                    has_copyright = check_copyright(
                        header_lines, args.copyright
                    )
                    output += " Copyright: " + format_success(has_copyright)
                    success = success and has_copyright

                has_license = check_license(header_lines)
                output += " License: " + format_success(has_license)
                success = success and has_license

            print(output)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    cli()
