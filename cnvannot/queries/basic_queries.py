from intervaltree import IntervalTree

from cnvannot.common.coordinates import GenomicCoordinates


def query_overlaps(db, query: GenomicCoordinates) -> bool:
    if query.chr in db:
        itree: IntervalTree = db[query.chr]
        if itree.overlaps(query.start, query.end):
            return True

    return False
