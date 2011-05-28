python-ips
----------

An IPS patching application with api, cli, and WinForms interfaces.

Basic Usage
-----------

Apply an IPS patch to a file.

::

    ./ips.py -f [file to patch] -p [ips patch]

Or on Windows, be sure to have python.exe on your path and run.

::

    python.exe ips.py -f [file to patch] -p [ips patch]

If you have IronPython 2.7 or newer installed, you can launch the python-ips GUI.

::

    ipy gui.py

Options
-------

Save a backup of the patched file.

::

    -b

Save a log.

::

    -l

Spoof a header for SNES patches which require them.

::

    --fake-header

