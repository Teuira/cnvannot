from cnvannot.common.coordinates import GenomicCoordinates
from cnvannot.queries.basic_queries import overlap_size


def dgv_gold_overlap_count_1_percent(db, query: GenomicCoordinates) -> int:
    res = 0
    if query.chr in db:
        if db[query.chr].overlaps(query.start, query.end):
            for r in db[query.chr][query.start:query.end]:
                t = r.data['var_type']
                if t != query.type:
                    continue
                if r.data['freq'] >= 1:
                    if overlap_size(r.begin, query.start, r.end, query.end) >= 0.7 * (query.end - query.start):
                        res = res + 1

    return res


def is_france_incomplete_penetrance(db, query: GenomicCoordinates) -> (bool, str):
    if query.chr in db:
        if db[query.chr].overlaps(query.start, query.end):
            for r in db[query.chr][query.start:query.end]:
                t = r.data['var_type']
                if t == query.type:
                    if overlap_size(r.begin, query.start, r.end, query.end) >= 0.7 * (query.end - query.start):
                        return True, r.data['desc']

    return False, ''


def exc_overlaps_70_percent(db, query: GenomicCoordinates) -> bool:
    if query.chr in db:
        if db[query.chr].overlaps(query.start, query.end):
            for r in db[query.chr][query.start:query.end]:
                if overlap_size(r.begin, query.start, r.end, query.end) >= 0.7 * (query.end - query.start):
                    return True

    return False
