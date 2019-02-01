import _ from 'lodash';

import { createFiltersFromMetadata } from '@/util';

// Only the fields of the model that are relevant for metadata
// conversion are included.
const model = {
    criteria: [
        { key: 'clot', type: 'toggle', default_date: '2017-07-01' },
        { key: 'bmi', type: 'toggle', default_date: null },
        { key: 'age', type: 'range' },
    ],
    ymcaSites: [
        { key: 'ymca_administrative' },
        { key: 'ymca_alexander' },
    ],
};

describe('createFiltersFromMetadata', () => {
    describe('parsing criteria', () => {
        describe('with unrecognized filter keys', () => {
            const metadata = {
                filters: {
                    foo: { date: '2018-01-01', value: 1 },
                },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with invalid date', () => {
            const metadata = {
                filters: {
                    clot: { date: 'foobar', value: 0 },
                },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with invalid value', () => {
            const metadata = {
                filters: {
                    clot: { date: '2017-01-01', value: 'foobar' },
                },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('missing required date', () => {
            const metadata = {
                filters: {
                    clot: { value: 0 },
                },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with date on non-date field', () => {
            const metadata = {
                filters: {
                    bmi: { date: '2018-01-01', value: 0 },
                },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with valid toggle filters', () => {
            const metadata = {
                filters: {
                    clot: { date: '2018-01-01', value: 1 },
                    bmi: 0,
                },
            };

            test('to convert values to booleans', () => {
                const { criteria } = createFiltersFromMetadata(model, metadata);

                expect(criteria.bmi).toEqual(false);
                expect(criteria.clot.value).toEqual(true);
            });
        });

        describe('with valid range filters', () => {
            const metadata = {
                filters: {
                    age: { min: '10', max: '25' },
                },
            };

            test('the filter is returned', () => {
                const { criteria } = createFiltersFromMetadata(model, metadata);

                expect(criteria.age).toEqual(metadata.filters.age);
            });
        });
    });

    describe('parsing YMCA sites', () => {
        describe('with invalid site', () => {
            const metadata = {
                ymca_sites: { foobar: 15 },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with invalid maxdist', () => {
            const metadata = {
                ymca_sites: { ymca_administrative: 'foobar' },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with valid sites', () => {
            const metadata = {
                ymca_sites: { ymca_administrative: 15 },
            };

            test('the site is converted to an object with site and value', () => {
                const { sites } = createFiltersFromMetadata(model, metadata);

                expect(_.isObject(sites.ymca_administrative)).toBeTruthy();
                expect(sites.ymca_administrative.site).toEqual('ymca_administrative');
                expect(sites.ymca_administrative.maxdist).toEqual(15);
            });
        });
    });

    describe('parsing result limits', () => {
        describe('with incorrect attributes', () => {
            const metadata = {
                patient_subset: { foobar: 15 },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('missing limit attribute', () => {
            const metadata = {
                patient_subset: { order_by: 'last_visit_date', order_asc: true },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('missing order_by attribute', () => {
            const metadata = {
                patient_subset: { limit: 100, order_asc: true },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('missing order_asc attribute', () => {
            const metadata = {
                patient_subset: { limit: 100, order_by: 'last_visit_date' },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with invalid limit', () => {
            const metadata = {
                patient_subset: { limit: 'foobar', order_by: 'last_visit_date', order_asc: true },
            };

            test('an error should be produced', () => {
                expect(() => createFiltersFromMetadata(model, metadata)).toThrow();
            });
        });

        describe('with valid data', () => {
            const metadata = {
                patient_subset: { limit: 100, order_by: 'last_visit_date', order_asc: true },
            };

            test('the patient_subset is returned', () => {
                const { limits } = createFiltersFromMetadata(model, metadata);

                expect(limits).toEqual(metadata.patient_subset);
            });
        });
    });
});
