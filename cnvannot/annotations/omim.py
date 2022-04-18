import os.path

from cnvannot.common.serialization import *


# OMIM DB

def omim_morbid_genes_load():
    gene_dict = {}

    omim_mg_base_file = '20181126_morbidGenes.tsv'
    omim_mg_base_path = os.path.join(Common.data_path, omim_mg_base_file)

    if serialization_is_serialized(omim_mg_base_file):
        return serialization_deserialize(omim_mg_base_file)

    with open(omim_mg_base_path) as f:
        for line in f:
            parts = line.split('\t')
            gene = parts[0]
            if parts[0] not in gene_dict:
                gene_dict[gene] = {"morbid": parts[1]}

    serialization_serialize(gene_dict, omim_mg_base_file)

    return gene_dict


def omim_query(refseq_db, query):
    pass