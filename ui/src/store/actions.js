import _ from 'lodash';

import { objectToArray } from '@/util';

import * as types from './mutation-types';


export default {
    setActiveFilters({ commit, dispatch }, { criteria, sites }) {
        commit(types.SET_ACTIVE_FILTERS, { criteria, sites });
        dispatch('getFilteredStats', criteria);
    },
    setActiveSites({ commit }, { sites }) {
        commit(types.SET_ACTIVE_YMCA_SITES, { sites });
    },
    loadUnfilteredStats({ commit }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats().then((result) => {
            const stats = _.mapValues(result, objectToArray);
            commit(types.LOAD_UNFILTERED_STATS, stats);
        });
    },
    getFilteredStats({ commit }, criteria) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats(criteria).then((result) => {
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
