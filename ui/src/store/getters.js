import _ from 'lodash';


export default {
    modelFilters: state => state.model.criteria,
    modelYmcaSites: state => state.model.ymcaSites,
    enabledYmcaSites: state => state.filters.ymcaSites,
    ymcaSiteByKey: state => key => _.find(state.model.ymcaSites, site => site.key === key),
};
