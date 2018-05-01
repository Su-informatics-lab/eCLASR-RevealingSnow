import * as types from './mutation-types';


export default {
    [types.LOAD_PATIENT_STATS](state, results) {
        state.ptstats = results;
    },
};
