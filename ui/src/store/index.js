import Vue from 'vue';
import Vuex from 'vuex';

import createLogger from 'vuex/dist/logger';

import actions from './actions';
import getters from './getters';
import mutations from './mutations';


Vue.use(Vuex);

const state = {
    stats: {
        unfiltered: [],
        filtered: [],
    },
    model: {
        criteria: [],
        ymcaSites: [],
        legend: null,
        version_details: null,
    },
    filters: {
        criteria: [],
        ymcaSites: [],
        limits: null,
    },
    featureFlags: {},
};

export default new Vuex.Store({
    state,
    actions,
    getters,
    mutations,
    strict: process.env.NODE_ENV !== 'production',
    plugins: process.env.NODE_ENV !== 'production' ? [createLogger()] : [],
});
