import _ from 'lodash';
import moment from 'moment';


function isDate(value) {
    return moment(value, 'YYYY-MM-DD', true).isValid();
}

function objectToArray(objdata) {
    return _.map(_.keys(objdata), key => ({
        name: key,
        value: objdata[key],
    }));
}


export { isDate, objectToArray };
