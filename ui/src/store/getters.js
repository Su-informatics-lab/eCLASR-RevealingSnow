import _ from 'lodash';
import * as d3 from 'd3-scale-chromatic';


function countPatients(data) {
    return _.sumBy(data.sex, 'value');
}

function getVersionDetails(data, key) {
    return _.find(data, { key });
}

const colors = d3.schemeCategory10;

export default {
    model: state => state.model,
    modelFilters: state => state.model.criteria,
    modelYmcaSites: state => state.model.ymcaSites,
    enabledCriteria: state => state.filters.criteria,
    enabledYmcaSites: state => state.filters.ymcaSites,
    ymcaSiteByKey: state => key => _.find(state.model.ymcaSites, site => site.key === key),
    patientCountUnfiltered: state => countPatients(state.stats.unfiltered),
    patientCountFiltered: state => countPatients(state.stats.filtered),
    getLegendObject: state => (key) => {
        if (state.model.legend === null) {
            return {};
        }

        const legend = state.model.legend[key];
        return _.keyBy(legend, 'key');
    },
    getLegendColor: state => (key) => {
        if (state.model.legend === null) {
            return {};
        }

        const legend = state.model.legend[key];
        return _.zipObject(_.map(legend, 'key'), colors);
    },
    getFeature: state => key => _.get(state.featureFlags, key, false),
    getApplicationVersion: state => getVersionDetails(state.model.version_details, 'app'),
};
