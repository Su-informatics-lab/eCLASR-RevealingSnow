import _ from 'lodash';
import { isDate } from './lang';


function criteriaValueToBoolean(value, key) {
    const valueAsString = _.toString(value);

    if (valueAsString === '0') {
        return false;
    }

    if (valueAsString === '1') {
        return true;
    }

    throw new Error(`invalid filter value ('${value}') for filter: ${key}`);
}

function validateToggleFilter(criteria, filter, key) {
    let validatedFilter = filter;

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

        validatedFilter.value = criteriaValueToBoolean(filter.value, key);
    } else {
        // Verify that the filter isn't an object
        if (_.isObject(filter)) {
            throw new Error(`date supplied for non-date filter: ${key}`);
        }

        validatedFilter = criteriaValueToBoolean(filter, key);
    }

    return validatedFilter;
}

function validateFilter(criteria, filter, key) {
    // Ensure that the filter is one in the model
    if (!_.has(criteria, key)) {
        throw new Error(`invalid filter key: ${key}`);
    }

    if (criteria[key].type === 'toggle') {
        return validateToggleFilter(criteria, filter, key);
    }

    return filter;
}

function getCriteriaFromMetadata(model, filters) {
    const modelCriteria = _.keyBy(model.criteria, 'key');

    return _.mapValues(filters, (filter, key) => validateFilter(modelCriteria, filter, key));
}

function getYmcaSitesFromMetadata(model, ymcaSites) {
    const modelSites = _.keyBy(model.ymcaSites, 'key');

    return _.mapValues(ymcaSites, (maxdist, key) => {
        // Ensure that the site is in the model
        if (!_.has(modelSites, key)) {
            throw new Error(`invalid site key: ${key}`);
        }

        // The maxdist must be numeric
        if (!_.isNumber(maxdist)) {
            throw new Error(`invalid maxdist (${maxdist}) for site: ${key}`);
        }

        return {
            site: key,
            maxdist,
        };
    });
}

function getLimitsFromMetadata(model, limits) {
    if (_.isEmpty(limits)) {
        return null;
    }

    const requiredKeys = ['limit', 'order_asc', 'order_by'];
    const missingKeys = _.reject(requiredKeys, _.partial(_.has, limits));

    if (missingKeys.length > 0) {
        throw new Error(`missing keys for limit: ${_.join(missingKeys, ', ')}`);
    }

    // Verify the limit value is numeric
    if (!_.isNumber(limits.limit)) {
        throw new Error(`limit value expected to be a number, was: ${limits.limit}`);
    }

    return limits;
}

function createFiltersFromMetadata(model, metadata) {
    const criteria = getCriteriaFromMetadata(model, _.get(metadata, 'filters', {}));
    const sites = getYmcaSitesFromMetadata(model, _.get(metadata, 'ymca_sites', {}));
    const limits = getLimitsFromMetadata(model, _.get(metadata, 'patient_subset', {}));

    return { criteria, sites, limits };
}


// eslint-disable-next-line import/prefer-default-export
export { createFiltersFromMetadata };
