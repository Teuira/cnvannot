import docker
from docker.errors import DockerException

# XCNV DB (ONLY hg19)
from cnvannot.common.coordinates import GenomicCoordinates
from cnvannot.annotations.base import base_coordinates_annotation


def xcnv_is_avail() -> bool:
    try:
        client = docker.from_env()
        images = client.images
    except DockerException:
        return False

    for img in images.list():
        if "xcnvcl" in str(img):
            return True

    return False


def xcnv_predict(query: GenomicCoordinates) -> str:
    if query.ref != "hg19":
        raise Exception("XCNV works only on hg19")

    res = ""  # TODO

    return base_coordinates_annotation(query)["xcnv": {"prediction": res}]
