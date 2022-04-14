from src.common.coordinates import GenomicCoordinates
from src.queries.basic_queries import query_overlaps


def hl_query_can_be_excluded_according_to_encode(db, query: GenomicCoordinates) -> bool:
    if query_overlaps(db, query):
        return True

    return False
