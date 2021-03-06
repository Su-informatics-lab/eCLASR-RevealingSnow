/* eslint-disable camelcase */

import * as types from './mutation-types';


export default {
    [types.LOAD_FILTERED_STATS](state, results) {
        state.stats.filtered = results;
    },
    [types.LOAD_UNFILTERED_STATS](state, results) {
        state.stats.unfiltered = results;
    },
    [types.LOAD_CRITERIA_DATA_MODEL](state, { filters, ymca_sites, legend, version_details }) {
        state.model.criteria = filters;
        state.model.ymcaSites = ymca_sites;
        state.model.legend = legend;
        state.model.version_details = version_details;
    },
    [types.SET_ACTIVE_FILTERS](state, { criteria, sites }) {
        state.filters.criteria = criteria;
        state.filters.ymcaSites = sites;
    },
    [types.SET_ACTIVE_YMCA_SITES](state, { sites }) {
        state.filters.ymcaSites = sites;
    },
    [types.SET_RESULT_LIMITS](state, { limits }) {
        state.filters.limits = limits;
    },
    [types.LOAD_FEATURE_FLAGS](state, flags) {
        state.featureFlags = flags;
    },
};
