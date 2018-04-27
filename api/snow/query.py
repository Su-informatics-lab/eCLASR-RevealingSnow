import logging

from flask import request

from snow import stats
from snow.ptscreen import pscr
from snow.util import make_json_response

logger = logging.getLogger(__name__)


# TODO: Validate Arguments
def patient_stats():
    logger.warning("TODO: Don't just trust the args; validate")
    patients = pscr.filter_patients(request.args)
    ptstats = stats.patient_counts_by_category(patients)

    return make_json_response(ptstats)
