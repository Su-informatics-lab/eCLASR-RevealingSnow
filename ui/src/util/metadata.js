import _ from 'lodash';
import { isDate } from './lang';


function isValidCriteriaValue(value) {
    const valueAsString = _.toString(value);

    // Must be 0 or 1
    return valueAsString === '0' || valueAsString === '1';
}

function validateFilter(criteria, filter, key) {
    let value;

    // Ensure that the filter is one in the model
    if (!_.has(criteria, key)) {
        throw new Error(`invalid filter key: ${key}`);
    }

    // Check if the model defines this criterion as being dated
    if (!_.isNull(criteria[key].default_date)) {
        // Verify that the filter specifies a date
        if (!_.has(filter, 'date')) {
            throw new Error(`missing required date for filter: ${key}`);
        }

        // Verify that the date is valid
        if (!isDate(filter.date)) {
            throw new Error(`invalid date format ('${filter.date}') for filter: ${key}`);
        }

        value = filter.value;
    } else {
        // Verify that the filter isn't an object
        if (_.isObject(filter)) {
            throw new Error(`date supplied for non-date filter: ${key}`);
        }

        value = filter;
    }

    // Verify that its value is valid
    if (!isValidCriteriaValue(value)) {
        throw new Error(`invalid filter value ('${value}') for filter: ${key}`);
    }
}

function getCriteriaFromMetadata(model, filters) {
    const modelCriteria = _.keyBy(model.criteria, 'key');

    return _.mapValues(filters, (filter, key) => {
        validateFilter(modelCriteria, filter, key);

        return filter;
    });
}

function getYmcaSitesFromMetadata(model, ymcaSites) {
    const modelSites = _.keyBy(model.ymcaSites, 'key');

    return _.mapValues(ymcaSites, (cutoff, key) => {
        // Ensure that the site is in the model
        if (!_.has(modelSites, key)) {
            throw new Error(`invalid site key: ${key}`);
        }

        // The cutoff must be numeric
        if (!_.isNumber(cutoff)) {
            throw new Error(`invalid cutoff (${cutoff}) for site: ${key}`);
        }

        return {
            site: key,
            cutoff,
        };
    });
}

function createFiltersFromMetadata(model, metadata) {
    const criteria = getCriteriaFromMetadata(model, _.get(metadata, 'filters', {}));
    const sites = getYmcaSitesFromMetadata(model, _.get(metadata, 'ymca_sites', {}));

    return { criteria, sites };
}


// eslint-disable-next-line import/prefer-default-export
export { createFiltersFromMetadata };
