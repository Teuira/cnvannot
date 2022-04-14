import os.path
import pickle


# OMIM DB

def omim_morbid_genes_load():
    gene_dict = {}
    omim_mg_base_dir = 'data'
    omim_mg_base_file = '20181126_morbidGenes.tsv'
    omim_mg_base_path = os.path.join(omim_mg_base_dir, omim_mg_base_file)

    serialized_path = os.path.join('serialized', omim_mg_base_file)
    if os.path.isfile(serialized_path):
        with open(os.path.join('serialized', omim_mg_base_file), 'rb') as f1:
            gene_dict = pickle.load(f1)
            return gene_dict

    with open(omim_mg_base_path) as f:
        for line in f:
            parts = line.split('\t')
            gene = parts[0]
            if parts[0] not in gene_dict:
                gene_dict[gene] = {"morbid": parts[1]}

    with open(os.path.join('serialized', omim_mg_base_file), 'wb') as f1:
        pickle.dump(gene_dict, f1)

    return gene_dict
