from cnvannot.annotations.xcnv import xcnv_interpretation_from_score


def interpretation_get(xcnv_score: float, exc_over: bool, gene_count: int, omim_gene_count: int,
                       dgv_gold_count: int, cnv_type: str) -> str:
    res = ''

    if dgv_gold_count > 0:
        return 'Since this variant overlaps one found in the DGV database, the variant could be considered benign'

    res += '' if exc_over is False else '\nThis variant overlaps an "Exclusion Region"' '\n' \
                                        'You may consider excluding it'
    if xcnv_score >= 0.5 and omim_gene_count == 0:
        res += 'Even if X-CNV score is high, meaning that this variant could be pathogenic,\n' \
               'no overlaps with known morbidity-associated genes have been reported,' '\n' \
               'hence, this variant could be benign'
    if res == '':
        res = xcnv_interpretation_from_score(xcnv_score).upper()

    res += "***\n\n*** The machine interpretation doesn't replace Human interpretation"

    return res
