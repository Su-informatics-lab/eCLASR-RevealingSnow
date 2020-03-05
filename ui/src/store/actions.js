import _ from 'lodash';

import { objectToArray } from '@/util';

import * as types from './mutation-types';


export default {
    setActiveFilters({ commit, dispatch }, { criteria, sites }) {
        commit(types.SET_ACTIVE_FILTERS, { criteria, sites });
        dispatch('getFilteredStats', { criteria, ymcaSites: sites });
    },
    setActiveSites({ commit, dispatch }, { sites }) {
        commit(types.SET_ACTIVE_YMCA_SITES, { sites });

        dispatch('reloadTotals');
    },
    setResultLimits({ commit, dispatch }, { limits }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.setResultLimits(limits);
        commit(types.SET_RESULT_LIMITS, { limits });

        dispatch('reloadTotals');
    },
    reloadTotals({ dispatch, state }) {
        // Need to reload everything
        dispatch('loadUnfilteredStats');
        dispatch('getFilteredStats', state.filters);
    },
    loadUnfilteredStats({ commit, state }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats({}, state.filters.ymcaSites).then((result) => {
            const stats = _.mapValues(result, objectToArray);
            commit(types.LOAD_UNFILTERED_STATS, stats);
        });
    },
    getFilteredStats({ commit }, { criteria, ymcaSites }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getPatientStats(criteria, ymcaSites).then((result) => {
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
    getFeatureFlags({ commit }) {
        // eslint-disable-next-line no-underscore-dangle
        this._vm.$api.getFeatureFlags().then((result) => {
            commit(types.LOAD_FEATURE_FLAGS, result);
        });
    },
};
