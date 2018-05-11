import _ from 'lodash';
import * as types from './mutation-types';


function objectToArray(objdata) {
    return _.map(_.keys(objdata), key => ({
        name: key,
        value: objdata[key],
    }));
}


export default {
    loadUnfilteredStats({ commit }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats().then((result) => {
            const stats = _.mapValues(result, objectToArray);
            commit(types.LOAD_UNFILTERED_STATS, stats);
        });
    },
    getFilteredStats({ commit }, filters) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats(filters).then((result) => {
            const stats = _.mapValues(result, objectToArray);
            commit(types.LOAD_FILTERED_STATS, stats);
        });
    },
    getCriteriaDataModel({ commit }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getCriteriaDataModel().then((result) => {
            commit(types.LOAD_CRITERIA_DATA_MODEL, result);
        });
    },
};
