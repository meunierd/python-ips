python-ips
----------

An IPS patching application with module, cli, and PyGUI interfaces.

Basic Usage
-----------

Apply an IPS patch to a file.

::
    ./ips.py -f [file to patch] -p [ips patch]

Or on Windows, be sure to have python.exe on your path and run.

::
    python.exe ips.py -f [file to patch] -p [ips patch]

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

