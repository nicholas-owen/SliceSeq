""" Run all the processing code to do all the analyses

Ideally, this will start with the reference files (at the moment, the FlyBase
GFF and FASTA files) and the sequence files in some kind of intelligent
structure, and generates all figures, tables, etc.

Let's see how far we can get...


"""
import subprocess as sp
import os
from glob import glob
import argparse as ap
from sys import stdout
import time

def make_multi():
    "Make a multi-genome fasta file"
    sp.call(['python', 'MakeMultigenome.py', 'Reference/AAA', 'mel', 'per',
              'wil', 'moj', 'vir'])
    #btb = sp.Popen(['bowtie-build', 'multi.fa', 'multi'])
    #bt2b = sp.Popen(['bowtie2-build', 'multi.fa', 'multi'])
    #btb.wait()
    #bt2b.wait()

def make_gtfs():
    "Make GTF files from all flybase GFF files"
    root = os.getcwd()
    os.chdir('Reference/AAA')

    for fname in glob('d*.gff'):
        print "Converting %s to GTF" % fname
        sp.call(['gffread', fname, '-E', '-T', '-o',
                  fname.replace('gff', 'gtf')])

    os.chdir(root)

def map_reads():
    "Call the do_tux program to run the tuxedo suite"
    sp.call(['python', 'MapReads.py'])

def assign_multireads():
    """Assign reads to species, using appropriate cutoff"""
    # Note that map reads currently does this!

    commandstr = ['python', 'AssignReads2.py']
    files = glob('analysis-multi/*/accepted_hits.bam')
    sp.call(commandstr + files)

def rescue_reads():
    """Rescue ambiguous reads and filter/reassign BAM tags

    For instance, reads where one end clearly maps to one species, but the other
    end may be ambiguous.

    More importantly, it fiddles with the BAM flags so that they are correct,
    based on what we have
    """

    commandstr = ['python', 'RescueAmbiguous.py']
    files = glob('analysis-multi/*/assigned_dmel.bam')
    sp.call(commandstr + files)


def main(args):
    """ Run all the sub-processing code"""

    if not('make_gtfs' in args.skiplist or '1' in args.skiplist):
        print '-'*72
        print "Making GTF files"
        print '-'*72
        print time.strftime("%Y-%m-%d %H:%M:%S -- %s since epoch")
        stdout.flush()
        make_gtfs()

    if not('make_genome' in args.skiplist or '2' in args.skiplist):
        print '-'*72
        print "Making Genome Mashups"
        print '-'*72
        print time.strftime("%Y-%m-%d %H:%M:%S -- %s since epoch")
        stdout.flush()
        make_multi()

    if not('map_reads' in args.skiplist or '3' in args.skiplist):
        print '-'*72
        print "Mapping reads"
        print '-'*72
        print time.strftime("%Y-%m-%d %H:%M:%S -- %s since epoch")
        stdout.flush()
        map_reads()

    #if not ('assign_reads' in args.skiplist or '4' in args.skiplist):
        #assign_multireads()

    if not ('rescue_reads' in args.skiplist or '5' in args.skiplist):
        print '-'*72
        print "Rescuing ambiguous reads"
        print '-'*72
        print time.strftime("%Y-%m-%d %H:%M:%S -- %s since epoch")
        stdout.flush()
        rescue_reads()
    
    if not ('calculate_abundances' in args.skiplist or '6' in args.skiplist):
        print '-'*72
        print "Calculating FPKM values"
        print '-'*72
        print time.strftime("%Y-%m-%d %H:%M:%S -- %s since epoch")
        stdout.flush()
        sp.call(['python', 'CalculateAbundances.py'])


def parse_args():
    """ Parse arguments from the commandline"""
    parser = ap.ArgumentParser()
    parser.add_argument('--skip', '-s', dest='skiplist', action='append',
                        default=[])
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
