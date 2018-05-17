import _ from 'lodash';


function countPatients(data) {
    return _.sumBy(data.sex, 'value');
}


export default {
    modelFilters: state => state.model.criteria,
    modelYmcaSites: state => state.model.ymcaSites,
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
};
