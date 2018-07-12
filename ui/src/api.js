import request from 'superagent';
import _ from 'lodash';


class Api {
    // noinspection JSUnusedGlobalSymbols
    static install(Vue, { endpoint, store }) {
        const api = new Api(endpoint);
        const apiProperty = {
            get() {
                return api;
            },
        };

        Object.defineProperty(Vue.prototype, '$api', apiProperty);

        if (store) {
            Object.defineProperty(store, '$api', apiProperty);
        }
    }

    constructor(endpoint) {
        this.endpoint = endpoint;
    }

    getPatientStats(filters) {
        return this.get('/stats', filters);
    }

    getYmcaStats(site, cutoff, filters) {
        const query = _.merge({ site, cutoff }, filters);
        return this.get('/ymca_stats', query);
    }

    getCriteriaDataModel() {
        return this.get('/model');
    }

    getExportUrl(filters) {
        const url = `${this.endpoint}/export`;
        let req = request.get(url);
        if (filters) {
            req = req.query(filters);
        }

        // Let SuperAgent do the heavy lifting of assembling the query URL
        // eslint-disable-next-line no-underscore-dangle
        req._finalizeQueryString();

        return req.url;
    }

    get(path, query) {
        const url = this.endpoint + path;
        let req = request.get(url);
        if (query) {
            req = req.query(query);
        }

        return new Promise((resolve, reject) => {
            req.set('Accept', 'application/json')
                .then((response) => {
                    resolve(response.body);
                }, (error) => {
                    reject(error);
                });
        });
    }
}


export default Api;
