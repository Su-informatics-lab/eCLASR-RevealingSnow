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
    setResultLimits({ commit, dispatch, state }, { limits }) {
        commit(types.SET_RESULT_LIMITS, { limits });

        // Need to reload everything
        dispatch('loadUnfilteredStats');
        dispatch('getFilteredStats', state.filters.criteria);
    },
    loadUnfilteredStats({ state, commit }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats({}, state.filters.limits).then((result) => {
            const stats = _.mapValues(result, objectToArray);
            commit(types.LOAD_UNFILTERED_STATS, stats);
        });
    },
    getFilteredStats({ state, commit }, criteria) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats(criteria, state.filters.limits).then((result) => {
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
