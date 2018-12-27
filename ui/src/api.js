import request from 'superagent';
import _ from 'lodash';


function flattenToDotNotation(filters) {
    return _.merge(..._.map(filters, (value, key) => {
        if (typeof value === 'object') {
            return _.mapKeys(value, (subvalue, subkey) => `${key}.${subkey}`);
        }

        return _.fromPairs([[key, value]]);
    }));
}

function buildQuery(criteria, limits) {
    const query = _.merge({}, criteria, limits);

    return flattenToDotNotation(query);
}

function buildMultipleYmcaSiteQuery(ymcaSites) {
    const sitesAndCutoffs = _.values(ymcaSites);
    const site = _.join(_.map(sitesAndCutoffs, 'site'), ',');
    const cutoff = _.join(_.map(sitesAndCutoffs, 'cutoff'), ',');

    return { site, cutoff };
}

function buildDownloadAndExportRequest(r, filters, exportOptions) {
    let req = r;
    const { criteria, ymcaSites } = filters;

    if (!_.isEmpty(criteria)) {
        req = req.query(flattenToDotNotation(criteria));
    }
    if (!_.isEmpty(ymcaSites)) {
        req = req.query(buildMultipleYmcaSiteQuery(ymcaSites));
    }
    if (!_.isEmpty(exportOptions)) {
        req = req.query(exportOptions);
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
        this.limits = null;
    }

    setResultLimits(limits) {
        // Not sure it really makes sense for this to be something the API keeps track of...
        this.limits = limits;
    }

    getPatientStats(criteria) {
        const query = buildQuery(criteria, this.limits);
        return this.get('/stats', query);
    }

    getYmcaStats(site, cutoff, criteria) {
        const query = _.merge({ site, cutoff }, buildQuery(criteria, this.limits));
        return this.get('/ymca_stats', query);
    }

    getCriteriaDataModel() {
        return this.get('/model');
    }

    getFeatureFlags() {
        return this.get('/features');
    }

    getDownloadUrl(filters, exportOptions) {
        const url = `${this.endpoint}/download`;
        let req = request.get(url);

        req = buildDownloadAndExportRequest(req, filters, exportOptions);

        // Let SuperAgent do the heavy lifting of assembling the query URL
        // eslint-disable-next-line no-underscore-dangle
        req._finalizeQueryString();

        return req.url;
    }

    exportToRemoteTrackingSystem(filters, exportOptions) {
        const url = `${this.endpoint}/export`;
        let req = request.post(url);

        req = buildDownloadAndExportRequest(req, filters, exportOptions);

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
