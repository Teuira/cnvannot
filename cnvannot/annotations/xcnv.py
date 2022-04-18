import docker
from docker.errors import DockerException

# XCNV DB (ONLY hg19)
from cnvannot.common.coordinates import GenomicCoordinates


def xcnv_is_avail() -> bool:
    client = None
    images = None

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

    res = ""
    pass

    return res
