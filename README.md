# ponos #
>**Ponos** (Ancient Greek: *Πόνος*; "toil"/"labour") was the god of hard labor
>and toil in Greek mythology.

## What is ponos ##
**ponos** is a Python script that helps you torture a given disk. It tries it best
to stress your disk by doing a loads of reads and writes.

It can be used to *preclear/burn-in* your harddrives before committing them to a storage
array. The goal is to root out bad disks before they are in production.

## Technical Details ##
**ponos** does sequential and random reads and writes. **ponos** operatis in
the following read/write phases:

1. Pre-read - We force the harddrives head to read for every sector on the
surface.

2. Full-write - **ponos** overwrites every sector with 0's from `/dev/zero`.
This erases all data on the drives (Well, if a block/sector already contains a
0', nothing will happen.).

3. Random writes - This is where we start making writes of random sizes
at random places on the disk.
  1. Small random writes - 50 writes of 0-200 blocks starting at a random block.
  2. Medium random writes - 20 writes of 2000-200000 blocks starting at a random block.

4. Random reads - This is where we start making reads of random sizes at random
places on the disk.
  1. Small random read - 50 reads of 0-200 blocks starting at a random block.
  2. Medium random read - 20 reads of 2000-200000 blocks starting at a random block.

5. Post-read - We, again, force the harddrives head to read every sector on the
surface of the disk.

**ponos** will look at the S.M.A.R.T. details of the disk before, and after the
above 5 steps. It will then compare said data and represent to you a FAILURE or
SUCCESS.

It will also display the statistics for each read and write, such as the time
it took and the size of the data.
