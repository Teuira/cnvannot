# Functions for parsing genomic coordinates

class GenomicCoordinates:
    chr = ''
    start = -1
    end = -1
    type = ''


def coordinates_from_string(query):
    ret_coordinates = GenomicCoordinates()
    query_chr = query.split(':')[0]
    query_start_end = query.split(':')[1].split('-')
    query_start = int(query_start_end[0])
    query_end = int(query_start_end[1])
    query_type = query.split(':')[2]
    ret_coordinates.chr = query_chr
    ret_coordinates.start = query_start
    ret_coordinates.end = query_end
    ret_coordinates.type = query_type
    return ret_coordinates
