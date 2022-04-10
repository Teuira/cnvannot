from intervaltree import IntervalTree


# RefSeq DB

def refseq_load():
    chr_dict = {}
    dgv_base_path = 'data/refGene.txt'
    with open(dgv_base_path) as f:
        for line in f:
            parts = line.split('\t')
            chrom = parts[2]
            start = int(parts[4])
            stop = int(parts[5])
            name1 = parts[1].lower()
            name2 = parts[12].lower()

            if chrom not in chr_dict:
                # Add new interval tree as value
                chr_dict[chrom] = IntervalTree()
            pass

    try:
        chr_dict[chrom][start:stop] = {'chr': chrom, 'start': start, 'stop': stop,
                                       'name1': name1, 'name2': name2}
    except ValueError:
        pass

    return chr_dict
