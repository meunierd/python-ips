import ips
from GUI import FileType, request_old_file, note_alert

ips_type = FileType(name = "IPS Patch", suffix = "ips")

ipspatch = request_old_file("Select IPS Patch", file_types=[ips_type])
topatch = request_old_file("Select File to Patch")

ips.apply(ipspatch.path, topatch.path)

note_alert("Patching %s successful." % topatch.name)
