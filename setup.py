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


from pathlib import Path
from setuptools import setup


SOURCE_ROOT = Path(__file__).parent
README = SOURCE_ROOT / "README.rst"


setup(
    name="apache-license-check",
    description="CLI tool to check source files for Apache License headers.",
    long_description=README.read_text(),
    url="https://faculty.ai/",
    author="Faculty",
    author_email="opensource@faculty.ai",
    license="Apache Software License",
    py_modules=["apache_license_check"],
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    install_requires=["termcolor"],
    entry_points={
        "console_scripts": ["apache-license-check=apache_license_check:cli"]
    },
    project_urls={
        "GitHub": "https://github.com/facultyai/apache-license-check"
    },
)
