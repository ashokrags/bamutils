import sys, copy


def process(fname):
    fin = open(fname)
    fixed_count = 0
    total_reads = 0

    for l in fin:
        line = copy.deepcopy(l).strip('\n')
        total_reads += 1
        if line[0] == '@':
            print line
            continue
        else:
            line = line.split("\t")
            if len(line[10]) != len(line[9]):
                sys.stderr.write(
                    "Dropping line !!! number of quality scores does not match number of bases: [%s] vs. [%s]" % (
                    line[9], line[10]) + "\n"
                    + line + "\n")
                # line[10] = 'O' * len(line[9])
            else:
                if check_illumina15_encoding(line[10]):
                    line[10] = illumina15_to_sanger(line[10])
                    print "\t".join(line)
                    fixed_count += 1
                else:
                    print "\t".join(line)

    sys.stderr.write("number of reads fixed: " + str(fixed_count))
    fin.close()


def check_illumina15_encoding(qual):
    encoded = False
    for q in qual:
        if ord(q) >= 76:
            encoded = True

    return encoded


def illumina15_to_sanger(qual):
    """
    Converts Illumina1.5+ (PhredB+64) to Sanger(Phred+33)
    """
    new_q = ''
    for q in qual:
        if (q == 'B'):
            new_q += '!'
        else:
            new_q += chr((ord(q) - 64) + 33)
    return new_q


def Illumina13_Sanger(qual):
    """
    Converts Illumina1.3+ (Phred+64) to Sanger(Phred+33)
    """
    new_q = ''
    for q in qual:
        new_q += chr((ord(q) - 64) + 33)
    return new_q


def Solexa_Sanger(qual):
    """
    Converts Solexa (PhredB+64) to Sanger(Phred+33)
    Need to adapt table from https://academic.oup.com/nar/article/38/6/1767/3112533
    """
    new_q = ''
    for q in qual:
        if (q == 'B'):
            new_q += '!'
        else:
            new_q += chr((ord(q) - 64) + 33)
    return new_q


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print >> sys.stderr, "usage (converts fastq solexa/1.3/1.5 to sanger): samtools view -h in.bam | bam_rescale_quals.py - | samtools view -bS - > out.bam"
    else:
        if sys.argv[1] == "-":
            sys.argv[1] = "/dev/stdin"
        process(sys.argv[1])
