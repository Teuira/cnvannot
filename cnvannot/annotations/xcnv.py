import docker
from docker.errors import DockerException
from time import sleep

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


def xcnv_predict(query: GenomicCoordinates) -> dict:
    if query.ref != "hg19":
        raise Exception("XCNV works only on hg19")

    client = docker.from_env()
    cont = client.containers.run('xcnvcl', query.chr + ':' + str(query.start) + '-' + str(query.end) + ':' + query.type,
                                 detach=True)

    prediction = ''

    for i in range(20):
        curr_out = cont.logs()
        if len(curr_out) > 0:
            possible_prediction = curr_out.split()[-1]
            try:
                float(possible_prediction)
            except ValueError:
                continue
            prediction = float(possible_prediction)
            break
        sleep(1)

    ret_dict = base_coordinates_annotation(query)
    ret_dict["xcnv"] = {"prediction": prediction}

    return ret_dict
