python-ips
----------

An IPS patching application with api, cli, and WinForms interfaces. Python 2/3
compatibility is supported.


Installation
------------

Install from PyPI:

::

    pip install python-ips

Or from the source-tree directory:

::

    python setup.py develop


Basic Usage
-----------

Apply an IPS patch to a file.

::

    python-ips PATCH TARGET 

Or on Windows, be sure to have python.exe on your path and run.

::

    python.exe ips.py PATCH TARGET


Options
-------

Save a backup of the patched file.

::

    -b --backup

Fake a SNES header

::

    --fake-header
