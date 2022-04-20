import gevent
from flask import Flask
from flask import render_template
from flask import jsonify

from cnvannot.annotations.dgv import dgv_gold_load
from cnvannot.annotations.encode import encode_load
from cnvannot.annotations.omim import omim_morbid_genes_load
from cnvannot.annotations.refseq import refseq_load
from cnvannot.annotations.ucsc import ucsc_get_annotation_link
from cnvannot.annotations.xcnv import *
from cnvannot.common.coordinates import coordinates_from_string
from cnvannot.queries.basic_queries import *
from cnvannot.queries.interpretation import interpretation_get
from cnvannot.queries.specific_queries import dgv_gold_overlap_count_1_percent

app = Flask(__name__)

dgv_db = dgv_gold_load()
refseq_db = refseq_load()
omim_mg_db = omim_morbid_genes_load()
encode_db = encode_load()
xcnv_avail = xcnv_is_avail()


@app.route("/", methods=['GET'])
def main_page():
    return render_template('home.html')


@app.route("/useful_links", methods=['GET'])
def useful_links():
    return render_template('links.html')


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/batch", methods=['GET'])
def batch():
    return render_template('batch.html')


@app.route("/search/<str_query>", methods=['GET'])
def search(str_query: str):
    query = coordinates_from_string(str_query)
    ucsc_url = str(ucsc_get_annotation_link(query)['ucsc']['link'])
    cnv_len = f'{(query.end - query.start):,}'
    cnv_type = str.upper(query.type)
    exclude_overlaps = query_overlaps(encode_db, query)
    gene_overlap_count = query_overlap_count(refseq_db, query)
    morbid_gene_overlap_count = query_overlap_count(omim_mg_db, query)
    dgv_gold_cnv_overlap_count = dgv_gold_overlap_count_1_percent(dgv_db, query)

    xcnv_res = None
    xcnv_res_interpretation = None
    if xcnv_avail:
        xcnv_res = xcnv_predict(query)['xcnv']['prediction']
        xcnv_res_interpretation = xcnv_interpretation_from_score(xcnv_res) + '\n'

    synth_interpretation = 'Interpretation suggestion(s): ' + interpretation_get(xcnv_res,
                                                                                 exclude_overlaps,
                                                                                 gene_overlap_count,
                                                                                 morbid_gene_overlap_count,
                                                                                 query.type)[0:-68]

    return jsonify({'ucsc_url': ucsc_url,
                    'cnv_len': cnv_len,
                    'cnv_type': cnv_type,
                    'exc_overlaps': exclude_overlaps,
                    'gene_overlap_count': gene_overlap_count,
                    'morbid_gene_overlap_count': morbid_gene_overlap_count,
                    'dgv_gold_cnv_overlap_count': dgv_gold_cnv_overlap_count,
                    'xcnv_res': xcnv_res,
                    'xcnv_res_interpretation': xcnv_res_interpretation,
                    'synth_interpretation': synth_interpretation})


def run_server():
    # dev server
    # app.run()
    # return

    # gevent (production)
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('', 5000), app)
    print('Server is running on: http://127.0.0.1:5000')
    http_server.serve_forever()
