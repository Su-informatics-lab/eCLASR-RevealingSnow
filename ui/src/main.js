// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Vue from 'vue';

import store from './store';

import App from './App';
import Api from './api';


const endpoint = process.env.API_ENDPOINT || '';
Vue.use(Api, { endpoint });


/* eslint-disable no-new */
new Vue({
    store,
    el: '#app',
    components: { App },
    template: '<App/>',
});
