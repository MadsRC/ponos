import tools
import sys
import time
import subprocess
import re
import datetime

####### TEST SECTION ##########
#sectorSize = 512
#sectorCount = 4194304      #2GiB
##sectorCount = 4294967296    #2TiB
#startOffset = 0
####### TEST SECTION ##########

if len(sys.argv) != 2:
    print "Too few arguments"
    sys.exit(1)
# Let's do some sanity checks on the input from the user. The argument should
# be the disk you want to torture.
a = re.compile("sd[a-z]")
if not a.match(sys.argv[1]):
    print "First argument needs to be sdX"
    sys.exit(1)
disk = sys.argv[1]
#disk = "sdb" # <-- DELETE ME, ONLY FOR TESTING!

# Print info about the disk choosed.
## Gather the info
sectorSize = tools.getSectorSize(disk)
sectorCount = tools.getSectorCount(disk)
startOffset = tools.getStartOffset(disk)
diskModel = tools.getDiskModelNumber(disk)
diskSerial = tools.getDiskSerial(disk)
## Print the info
print "+"+"-"*55+"+"
print "[-] Disk Model: %s" % (diskModel,)
print "[-] Disk Serial: %s" % (diskSerial,)
print "[-] Physical sector size: %s" % (sectorSize,)
print "[-] Sector count: %s" % (sectorCount,)
print "[-] Start offset: %s" % (startOffset,)

# Here should be a warning that the disk WILL BE DESTROYED
print "+"+"-"*55+"+"
print "WARNING! Disk /dev/%s will be destroyed!" % (disk)
print "+"+"-"*55+"+"
print "[!] Are you absolutely sure this is the right one?"
user_in = raw_input("[yes|no]: ")
if user_in != "yes":
    sys.exit("Exiting, you did not type 'yes'")

# Start timing the script. We do so after user input, as the time you'd take
# deciding wether or not it's the right disk, shouldn't be part of the scripts
# run time calculation.
script_time_start = datetime.datetime.now()
# Get preliminary SMART data/status
print "+"+"-"*55+"+"
print "[-] Retrieving preliminary S.M.A.R.T. data"
start_SMART = tools.getSMARTattributes(disk)

# Pre-Read the disk
print "+"+"-"*55+"+"
print "[-] Pre-Reading"
before = datetime.datetime.now()
tools.dd("/dev/%s" % (disk,), "/dev/null", sectorSize, 0, 0)
after = datetime.datetime.now()
total = after-before
print "[+] Pre-Read done in %i seconds" % (total.total_seconds(),)

# Write 0's to the entire disk.
print "+"+"-"*55+"+"
print "[-] Full-write"
before = datetime.datetime.now()
tools.dd("/dev/zero", "/dev/%s" % (disk,), sectorSize, 0, 0)
after = datetime.datetime.now()
total = after-before
print "[+] Wrote 0's to entire disk in %i seconds" % (total.total_seconds(),)

# Random Writes
print "+"+"-"*55+"+"
print "[-] Random writes"

# Small random writes (0 - 200 sectors/blocks)
count = 1
while count < 201:
    before = datetime.datetime.now()
    dd_params = tools.genWrite(sectorSize, sectorCount, startOffset, 0, 200)
    tools.dd("/dev/zero", "/dev/%s" % (disk,), sectorSize, dd_params[0], 0, dd_params[1])
    after = datetime.datetime.now()
    total = after-before
    print "[+] Small random write #%i done in %i ms - Wrote %i blocks" % (count,total.total_seconds()*1000,dd_params[1],)
    count = count+1

# Medium random writes (2000 - 200000 sectors/blocks)
count = 1
while count < 101:
    before = datetime.datetime.now()
    dd_params = tools.genWrite(sectorSize, sectorCount, startOffset, 20000, 200000)
    tools.dd("/dev/zero", "/dev/%s" % (disk,), sectorSize, dd_params[0], 0, dd_params[1])
    after = datetime.datetime.now()
    total = after-before
    print "[+] Medium random write #%i done in %i ms - Wrote %i blocks" % (count,total.total_seconds()*1000,dd_params[1]*sectorSize,)
    count = count+1

# Random Reads
print "+"+"-"*55+"+"
print "Random reads"

# Small random reads (0 - 200 sectors/blocks)
count = 1
while count < 201:
    before = datetime.datetime.now()
    dd_params = tools.genWrite(sectorSize, sectorCount, startOffset, 0, 200)
    tools.dd("/dev/%s" % (disk,), "/dev/null", sectorSize, 0, dd_params[0], dd_params[1])
    after = datetime.datetime.now()
    total = after-before
    print "[+] Small random read #%i done in %i ms - Read %i blocks" % (count,total.total_seconds()*1000,dd_params[1],)
    count = count+1

# Medium random reads (2000 - 200000 sectors/blocks)
count = 1
while count < 101:
    before = datetime.datetime.now()
    dd_params = tools.genWrite(sectorSize, sectorCount, startOffset, 20000, 200000)
    tools.dd("/dev/%s" % (disk,), "/dev/null", sectorSize, 0, dd_params[0], dd_params[1])
    after = datetime.datetime.now()
    total = after-before
    print "[+] Medium random read #%i done in %i ms - Read %i blocks" % (count,total.total_seconds()*1000,dd_params[1],)
    count = count+1

# Post-Read the disk
print "+"+"-"*55+"+"
print "[-] Post-read"
before = datetime.datetime.now()
tools.dd("/dev/%s" % (disk,), "/dev/null", sectorSize, 0, 0)
after = datetime.datetime.now()
total = after-before
print "[+] Post-read done in %i seconds" % (total.total_seconds(),)

# Get SMART data/status
print "+"+"-"*55+"+"
print "[-] Retrieving final S.M.A.R.T. data"
end_SMART = tools.getSMARTattributes(disk)

# Compare SMART data/status
print "+"+"-"*55+"+"
print "[-] Comparing S.M.A.R.T. data"
print ""
print "S.M.A.R.T. data pre script:"
print start_SMART
print ""
print "S.M.A.R.T. data post script:"
print end_SMART

# Displaying the final verdict
print "+"+"-"*55+"+"
script_time_done = datetime.datetime.now()
total = script_time_done-script_time_start
print "[-] ponos done."
print "[-] This session lasted for %s seconds." % (total.total_seconds(),)
