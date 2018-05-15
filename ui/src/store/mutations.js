/* eslint-disable camelcase */

import * as types from './mutation-types';


export default {
    [types.LOAD_FILTERED_STATS](state, results) {
        state.stats.filtered = results;
    },
    [types.LOAD_UNFILTERED_STATS](state, results) {
        state.stats.unfiltered = results;
    },
    [types.LOAD_CRITERIA_DATA_MODEL](state, { filters, ymca_sites }) {
        state.criteria = filters;
        state.ymcaSites = ymca_sites;
    },
};
