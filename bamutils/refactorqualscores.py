import sys

def process(fname):
    fin = open(fname)

    for line in fin:
        if line[0] == '@':
            print line,
            continue
        else:
            line = line.strip().split("\t")
            if len(line[10]) != len(line[9]):
                print >> sys.stderr, "number of quality scores does not match number of bases: [%s] vs. [%s]" % (
                line[9], line[10])
                line[10] = 'O' * len(line[9])
            else:
                if check_illumina15_encoding(line[10]):
                    line[10] = illumina15_Sanger(line[10])

            print "\t".join(line)
    fin.close()

def check_illumina15_encoding(qual):
    encoded = False
    for q in qual:
        if ord(q) >= 74:
            encoded = True
        return encoded

def Illumina15_Sanger(qual):
        """
        Converts Illumina1.5+ (PhredB+64) to Sanger(Phred+33)
        """
        new_q=''
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
        print >>sys.stderr, "usage (converts fastq solexa/1.3/1.5 to sanger): samtools view -h in.bam | bam_rescale_quals.py - | samtools view -bS - > out.bam"
    else:
        if sys.argv[1] == "-":
            sys.argv[1] = "/dev/stdin"
        process(sys.argv[1])