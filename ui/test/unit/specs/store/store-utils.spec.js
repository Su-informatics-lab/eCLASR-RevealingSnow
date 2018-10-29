import _ from 'lodash';

import { createFiltersFromMetadata } from '@/store/store-utils';

// Only the fields of the model that are relevant for metadata
// conversion are included.
const model = {
    criteria: [
        { key: 'clot', default_date: '2017-07-01' },
        { key: 'bmi', default_date: null },
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

        describe('with valid filters', () => {
            const metadata = {
                filters: {
                    clot: { date: '2018-01-01', value: 1 },
                    bmi: 1,
                },
            };

            test('to match the input', () => {
                const { criteria } = createFiltersFromMetadata(model, metadata);

                expect(_.isEqual(criteria, metadata.filters)).toBeTruthy();
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

        describe('with invalid cutoff', () => {
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
                expect(sites.ymca_administrative.cutoff).toEqual(15);
            });
        });
    });
});
