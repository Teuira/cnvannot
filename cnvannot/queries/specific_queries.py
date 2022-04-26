from cnvannot.common.coordinates import GenomicCoordinates


def dgv_gold_overlap_count_1_percent(db, query: GenomicCoordinates) -> int:
    res = 0
    if query.chr in db:
        if db[query.chr].overlaps(query.start, query.end):
            for r in db[query.chr][query.start:query.end]:
                t = r.data['var_type']
                if t != query.type:
                    continue
                if r.data['freq'] >= 1:
                    res = res + 1

    return res


def is_france_incomplete_penetrance(db, query: GenomicCoordinates) -> (bool, str):
    if query.chr in db:
        if db[query.chr].overlaps(query.start, query.end):
            for r in db[query.chr][query.start:query.end]:
                t = r.data['var_type']
                if t == query.type:
                    return True, r.data['desc']

    return False, ''
