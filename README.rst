Apache License Check
====================

A command line tool for checking if the source files of a Python project have
Apache License headers.

Install
-------

.. code-block:: bash

    pip install apache-license-check

Usage
-----

To check all Python files recursively under the current directory:

.. code-block:: bash

    apache-license-check

Optionally, pass one or more files or directories to check:

.. code-block:: bash

    apache-license-check setup.py myproject/

You can also check that files include a copyright statement with the
``--copyright`` flag. Pass a substring (such as the name of the copyright
holder) to check:

.. code-block:: bash

    apache-license-check setup.py --copyright "Faculty Science Limited"
