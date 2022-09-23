from intervaltree import IntervalTree

from cnvannot.common.serialization import *


# DGV DB

def dgv_full_load():
    chr_dict = {}

    dgv_base_file = 'GRCh37_hg19_variants_2020-02-25.txt'
    dgv_base_path = os.path.join(Common.data_path, dgv_base_file)

    if serialization_is_serialized(dgv_base_file):
        return serialization_deserialize(dgv_base_file)

    with open(dgv_base_path) as f:
        for line in f:
            if line.startswith("variantaccession"):
                continue
            parts = line.split('\t')
            chrom = 'chr' + parts[1]
            start = int(parts[2])
            stop = int(parts[3])
            var_type = parts[5].lower()

            if 'gain' in var_type or 'duplication' in var_type:
                var_type = 'GAIN'
            elif 'loss' in var_type or 'deletion' in var_type:
                var_type = 'LOSS'

            if chrom not in chr_dict:
                # Add new interval tree as value
                chr_dict[chrom] = IntervalTree()

            try:
                chr_dict[chrom][start:stop] = {'chr': chrom, 'start': start, 'stop': stop,
                                               'var_type': var_type}
            except ValueError:
                pass

    serialization_serialize(chr_dict, dgv_base_file)

    return chr_dict


def dgv_gold_load():
    chr_dict = {}

    dgv_base_file = 'DGV.GS.March2016.50percent.GainLossSep.Final.hg19.gff3'
    dgv_base_path = os.path.join(Common.data_path, dgv_base_file)

    if serialization_is_serialized(dgv_base_file):
        return serialization_deserialize(dgv_base_file)

    with open(dgv_base_path) as f:
        for line in f:
            parts = line.split('\t')
            chrom = parts[0]
            start = int(-1)
            stop = int(-1)
            dat = parts[8]
            dat_parts = dat.split(';')
            for dp in dat_parts:
                if dp.startswith('outer_start'):
                    start = int(dp.split('=')[1])
                if dp.startswith('outer_end'):
                    stop = int(dp.split('=')[1])
                    break
            # Sanity check for start and end
            if start == -1 or stop == -1:
                raise Exception('Start and/or stop not assigned!')

            var_type = ''
            freq_percent = ''
            for dp in dat_parts:
                if dp.startswith('variant_sub_type'):
                    var_type = dp.split('=')[1]
                if dp.startswith('Frequency'):
                    freq_percent = float(dp.split('=')[1][:-1])
            if var_type == 'Gain':
                var_type = 'GAIN'
            elif var_type == 'Loss':
                var_type = 'LOSS'
            if var_type == '':
                print("Cannot parse line")

            if chrom not in chr_dict:
                # Add new interval tree as value
                chr_dict[chrom] = IntervalTree()

            try:
                chr_dict[chrom][start:stop] = {'chr': chrom, 'start': start, 'stop': stop,
                                               'var_type': var_type, 'freq': freq_percent}
            except ValueError:
                pass

    serialization_serialize(chr_dict, dgv_base_file)

    return chr_dict
