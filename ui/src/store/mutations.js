import * as types from './mutation-types';


export default {
    [types.LOAD_PATIENT_STATS](state, results) {
        state.ptstats = results;
    },
    [types.LOAD_CRITERIA_DATA_MODEL](state, { filters }) {
        state.filters = filters;
    },
};
