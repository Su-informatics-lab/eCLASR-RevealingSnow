import Vue from 'vue';
import Vuex from 'vuex';

import createLogger from 'vuex/dist/logger';

import actions from './actions';
import getters from './getters';
import mutations from './mutations';


Vue.use(Vuex);

const state = {
    ptstats: [],
    filters: [],
};

export default new Vuex.Store({
    state,
    actions,
    getters,
    mutations,
    strict: process.env.NODE_ENV !== 'production',
    plugins: process.env.NODE_ENV !== 'production' ? [createLogger()] : [],
});
