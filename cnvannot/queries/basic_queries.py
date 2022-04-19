from intervaltree import IntervalTree

from cnvannot.common.coordinates import GenomicCoordinates


def query_overlaps(db, query: GenomicCoordinates) -> bool:
    if query.chr in db:
        itree: IntervalTree = db[query.chr]
        if itree.overlaps(query.start, query.end):
            return True

    return False


def query_overlap_count(db, query: GenomicCoordinates) -> int:
    if not query_overlaps(db, query):
        return 0
    count = 0
    if query.chr in db:
        itree: IntervalTree = db[query.chr]
        count = len(itree[query.start:query.end])

    return count
