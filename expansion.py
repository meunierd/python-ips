#!/usr/bin/env python

from binascii import unhexlify
import md5

__author__ = "Devon Meunier"
__email__ = "devon.meunier@utoronto.ca"
__license__ = "MIT"
__version__ = "0.1"

def get_md5(source):
    """Return the MD5 hash of the file `source`."""
    m = md5.new()
    while True:
        d = source.read(8196)
        if not d: break
        m.update(d)
    return m.hexdigest()

def hex_to_bstr(d):
    """Return the bytestring equivalent of a plain-text hex value."""
    if len(d) % 2: d = "0" + d
    return unhexlify(d)

def load_line(s):
    """Tokenize a tab-delineated string and return as a list."""
    return s.strip().split('\t')

def load_script():
    script = {}
    script["file"] = "ROM Expander Pro.txt"
    with open(script["file"]) as script_file:
        script_lines = script_file.readlines()

    # Load the `NAME` line from script.
    l = load_line(script_lines.pop(0))
    assert 'NAME' == l.pop(0)
    script["source"], script["target"] = l
    assert script["target"] != script["source"]

    # Load the `SIZE` and optional `MD5`
    l = load_line(script_lines.pop(0))
    script["old_size"] = eval("0x" + l[1])
    script["new_size"] = eval("0x" + l[2])
    if l.index(l[-1]) > 2: script["MD5"] = l[3].lower()

    # Load the replacement `HEADER`.
    l = load_line(script_lines.pop(0))
    assert 'HEADER' == l.pop(0) 
    script["header_size"] = eval("0x" + l.pop(0))
    assert script["header_size"] > len(l)
    # Sanitize and concatenate the header data.
    new_header = "".join(["0" * (2 - len(x)) + x for x in l])
    # Cast to character data and pad with 0x00 to header_size
    new_header = hex_to_bstr(new_header)
    script["header"] = new_header + "\x00" * (script["header_size"] - len(l))

    # Check the source file MD5.
    if "MD5" in script:
        with open(script["source"], "rb") as s_file:
            # Don't digest the header.
            s_file.read(script["header_size"])
            assert script["MD5"] == get_md5(s_file) 

    script["ops"] = []
    while script_lines:
        script["ops"].append(load_line(script_lines.pop(0)))

    return script

def expand_rom(script):
    with open(script["source"], "rb") as s, open(script["target"], "wb") as t:

        def copy(a, b):
            source_ptr = script["header_size"] + a
            write_ptr = script["header_size"] + b
            s.seek(source_ptr)
            t.seek(write_ptr)
            t.write(s.read(end_ptr - write_ptr))

        def replace(a, b):
            pass # maybe do this in a second pass

        def fill(destination, value):
            write_ptr = script["header_size"] + destination
            t.seek(write_ptr)
            t.write(value * (end_ptr - write_ptr))
            
        # Write Header
        t.write(script["header"])

        while script["ops"]:
            op = script["ops"].pop(0)
            cmd = op.pop(0)

            if not script["ops"]:
                end_ptr = script["header_size"] + script["new_size"]
            else:
                end_ptr = eval("0x" + script["ops"][0][1]) + \
                          script["header_size"]

            if cmd == "COPY":
                copy(eval("0x" + op[1]), eval("0x" + op[0]))
           
            elif cmd == "FILL":
                fill(eval("0x" + op[0]),
                     hex_to_bstr(op[1]))

            elif cmd == "REPLACE": pass

script = load_script()
expand_rom(script)
