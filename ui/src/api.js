import request from 'superagent';


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

    getCriteriaDataModel() {
        return this.get('/model');
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
