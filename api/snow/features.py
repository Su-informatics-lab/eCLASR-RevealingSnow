from snow import constants as C
from snow.util import make_json_response


def _create_feature_flags():
    from snow.tracking import tracking

    return {
        C.TRACKING_API_ENABLED: tracking.enabled
    }


def get_feature_flags():
    flags = _create_feature_flags()
    return make_json_response(flags)
