import request from 'superagent';
import _ from 'lodash';


function buildMultipleYmcaSiteQuery(ymcaSites) {
    const sitesAndCutoffs = _.values(ymcaSites);
    const site = _.join(_.map(sitesAndCutoffs, 'site'), ',');
    const cutoff = _.join(_.map(sitesAndCutoffs, 'cutoff'), ',');

    return { site, cutoff };
}

function buildDownloadAndExportRequest(r, filters, limit) {
    let req = r;
    const { criteria, ymcaSites } = filters;

    if (!_.isEmpty(criteria)) {
        req = req.query(criteria);
    }
    if (!_.isEmpty(ymcaSites)) {
        req = req.query(buildMultipleYmcaSiteQuery(ymcaSites));
    }
    if (!_.isEmpty(limit)) {
        req = req.query(limit);
    }

    return req;
}


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

    getDownloadUrl(filters, limit) {
        const url = `${this.endpoint}/download`;
        let req = request.get(url);

        req = buildDownloadAndExportRequest(req, filters, limit);

        // Let SuperAgent do the heavy lifting of assembling the query URL
        // eslint-disable-next-line no-underscore-dangle
        req._finalizeQueryString();

        return req.url;
    }

    exportToRemoteTrackingSystem(filters, limit) {
        const url = `${this.endpoint}/export`;
        let req = request.post(url);

        req = buildDownloadAndExportRequest(req, filters, limit);

        return new Promise((resolve, reject) => {
            req.set('Accept', 'application/json')
                .then((response) => {
                    resolve(response.body);
                }, (error) => {
                    reject(error);
                });
        });
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
