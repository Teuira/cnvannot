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


def xcnv_predict(queries) -> list:
    xcnv_query = ''
    for q in queries:
        if q.ref != 'hg19':
            raise Exception('XCNV works only on hg19')
        xcnv_query += q.chr + ':' + str(q.start) + '-' + str(q.end) + ':' + q.type + ','
    xcnv_query = xcnv_query[:-1]

    client = docker.from_env()

    cont = client.containers.run('xcnvcl', xcnv_query, detach=True)

    prediction_float = []
    timeout = True

    # Wait loop.
    for i in range(300):
        curr_out = cont.logs()
        if len(curr_out) > 0:
            # Output received.
            timeout = False
            possible_prediction = curr_out.split()[-1]
            prediction_parts = possible_prediction.decode('ascii').split(',')
            sanity_check_count = int(prediction_parts[0])
            if len(prediction_parts) != (sanity_check_count + 1):
                raise Exception("X-CNV sanity check failed!")

            for p in prediction_parts[1:]:
                prediction_float.append(float(p))

            break
        sleep(1)

    if timeout:
        raise Exception("Timeout Exception")

    ret_dict_list = []
    for i in range(len(queries)):
        ret_dict = base_coordinates_annotation(queries[i])
        ret_dict["xcnv"] = {"prediction": prediction_float[i]}
        ret_dict_list.append(ret_dict)

    return ret_dict_list


def xcnv_interpretation_from_score(score: float) -> str:
    if score < 0.25:
        return 'benign'
    elif score < 0.5:
        return 'likely benign'
    elif score < 0.75:
        return 'likely pathogenic'
    else:
        return 'pathogenic'
