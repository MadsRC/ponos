import random
import subprocess

def genWrite(sectorSize, sectorCount, startOffset, writeSizeMin, writeSizeMax):
    ''' Generate the parameters used in dd to create a random write of specified size.
    The writeSizeMin and writeSizeMax should be of type int, and together they form
    the range used to determien the size of the generate write parameters.

    It returns a list, where index 0 should be used in GNU dd's 'seek' and 1
    should be used in GNU dd's 'count'.
    '''
    loop = True
    while loop:
        availSectors = sectorCount-startOffset
        seekStart = random.randint(0, availSectors)
        remainingSectors = availSectors - seekStart
        blockCount = random.randint(writeSizeMin, writeSizeMax)
        writeEndsAtSector = blockCount+seekStart
        if writeEndsAtSector < availSectors:
            loop = False
    output = []
    output.append(seekStart)
    output.append(blockCount)
    return output

def getSectorSize(disk):
	proc = subprocess.Popen(["cat", "/sys/block/%s/queue/physical_block_size" % disk], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = proc.communicate()
	return int(out.rstrip("\n"))

def getSectorCount(disk):
	cmd = "hdparm -g /dev/%s | tail -n1 | cut -d ' ' -f 12" % (disk,)
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = proc.communicate()
	return int(out.replace(",","").rstrip("\n"))

def getStartOffset(disk):
	cmd = "hdparm -g /dev/%s | tail -n 1 | cut -d ' ' -f 15" % (disk,)
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = proc.communicate()
	return int(out.rstrip("\n"))

def getDiskModelNumber(disk):
    cmd = "hdparm -I /dev/%s | grep 'Model Number:' | tr -d ' ' | sed 's/ModelNumber://g'" % (disk,)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.strip().rstrip("\n")

def getDiskSerial(disk):
    cmd ="hdparm -I /dev/%s | grep 'Serial Number:' | tr -d ' ' | sed 's/SerialNumber://g'" % (disk,)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.strip().rstrip("\n")

def dd(inputfile, outputfile, blocksize, seek, skip, count=None):
    ''' dd wrapper function.
    Input and output file should be a full path to the
    devices. blocksize, seek, skip and count is blocks represented as integers.
    If you need a read or write of the entire disk, do not specify a count
    value.

    From GNU dd:
    if=file
        Read from file instead of standard input.
    of=file
        Write to file instead of standard output. Unless conv=notrunc is
        given, dd truncates file to zero bytes (or the size specified with
        seek=).
    bs=bytes
        Set both input and output block sizes to bytes. This makes dd read and
        write bytes per block, overriding any ibs and obs settings. In
        addition, if no data-transforming conv option is specified, input is
        copied to the output as soon as it's read, even if it is smaller than
        the block size.
    skip=n
        Skip n ibs-byte blocks in the input file before copying. If
        iflag=skip_bytes is specified, n is interpreted as a byte count rather
        than a block count.
    seek=n
        Skip n obs-byte blocks in the output file before copying. if
        oflag=seek_bytes is specified, n is interpreted as a byte count
        rather than a block count.
    count=n
        Copy n ibs-byte blocks from the input file, instead of
        everything until the end of the file. if iflag=count_bytes is
        specified, n is interpreted as a byte count rather than a block
        count. Note if the input may return short reads as could be the
        case when reading from a pipe for example, iflag=fullblock
        will ensure that count= corresponds to complete input blocks
        rather than the traditional POSIX specified behavior of counting
        input read operations.
    '''
    if count == None:
        proc = subprocess.Popen(["dd", "if=%s" % inputfile, "of=%s" % \
        outputfile, "bs=%i" % blocksize, "seek=%i" % seek, "skip=%i" % skip], \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
    else:
        proc = subprocess.Popen(["dd", "if=%s" % inputfile, "of=%s" % outputfile, \
        "bs=%i" % blocksize, "seek=%i" % seek, "skip=%i" % skip, "count=%i" % \
        count], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
    return err

def getSMARTattributes(disk):
    cmd ="smartctl --attributes /dev/%s" % (disk,)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.rstrip("\n")
