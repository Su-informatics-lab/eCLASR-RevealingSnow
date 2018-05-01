import * as types from './mutation-types';


export default {
    getPatientStats({ commit }, filters) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats(filters).then((result) => {
            commit(types.LOAD_PATIENT_STATS, result);
        });
    },
};
