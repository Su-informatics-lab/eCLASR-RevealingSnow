import logging

from flask import request

from snow import stats, ymca
from snow.ptscreen import pscr
from snow.request import parse_query
from snow.util import make_json_response

logger = logging.getLogger(__name__)


def patient_stats():
    query = parse_query(request.args, site_required=False)

    patients = pscr.filter_patients(query)
    ptstats = stats.patient_counts_by_category(patients)

    return make_json_response(ptstats)


def ymca_stats():
    query = parse_query(request.args)

    patients = pscr.filter_patients(query)
    dist_stats = ymca.get_ymca_distance_stats(
        patients, query.sites.sites, query.sites.cutoffs, ymca.YMCA_DEMOGRAPHIC_CATEGORIES
    )

    return make_json_response(dist_stats)
