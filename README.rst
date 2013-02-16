python-ips
----------

An IPS patching application with api, cli, and WinForms interfaces. Python 2/3
compatibility is supported.

Basic Usage
-----------

Apply an IPS patch to a file.

::

    ./ips PATCH TARGET 

Or on Windows, be sure to have python.exe on your path and run.

::

    python.exe ips.py PATCH TARGET


Options
-------

Save a backup of the patched file.

::

    -b --backup
