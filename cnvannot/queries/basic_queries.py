from intervaltree import IntervalTree

from cnvannot.common.coordinates import GenomicCoordinates


def overlap_size(sta1, sta2, end1, end2):
    return max(0, min(end1, end2) - max(sta1, sta2) + 1)


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
