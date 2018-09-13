import Vue from 'vue';
import _ from 'lodash';

import BarChart from '@/components/charts/BarChart';


const props = {
    data: {},
    width: 0,
    height: 0,
};

function objectToArray(objdata) {
    return _.map(_.keys(objdata), key => ({
        name: key,
        value: objdata[key],
    }));
}

describe('BarChart.vue', () => {
    let chart;

    describe('with only required props', () => {
        beforeEach(() => {
            const Constructor = Vue.extend(BarChart);
            chart = new Constructor({ propsData: props }).$mount();
        });

        test('the chart object should not be null', () => {
            expect(chart.chart).not.toBeNull();
        });

        test('the initial chart data should be empty', () => {
            expect(_.isEmpty(chart.chart.data())).toBeTruthy();
        });

        test('setting data creates categories on the chart object', () => {
            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
                bar: objectToArray({ a: 4, b: 5, c: 6 }),
            });

            const data = chart.chart.data();
            expect(data).toHaveLength(2);

            expect(data[0].id).toEqual('foo');
            expect(data[0].values).toHaveLength(3);

            expect(data[1].id).toEqual('bar');
            expect(data[1].values).toHaveLength(3);
        });

        test('setting new data with missing category removes absent category', () => {
            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
                bar: objectToArray({ a: 4, b: 5, c: 6 }),
            });

            chart.setData({
                foo: objectToArray({ a: 1, b: 2 }),
            });

            const data = chart.chart.data();
            expect(data).toHaveLength(1);

            expect(data[0].id).toEqual('foo');
            expect(data[0].values).toHaveLength(2);
        });

        test('setting new data with missing category removes absent category', () => {
            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
                bar: objectToArray({ a: 4, b: 5, c: 6 }),
            });

            chart.setData({
                foo: objectToArray({ a: 1, b: 2 }),
            });

            const data = chart.chart.data();
            expect(data).toHaveLength(1);

            expect(data[0].id).toEqual('foo');
            expect(data[0].values).toHaveLength(2);
        });
    });

    describe('with group legend', () => {
        beforeEach(() => {
            const Constructor = Vue.extend(BarChart);
            const propsWithLegend = {
                data: {},
                width: 0,
                height: 0,
                groupLegend: {
                    foo: 'Foo',
                    bar: 'Bar',
                },
            };

            chart = new Constructor({ propsData: propsWithLegend }).$mount();
        });

        test('setting data uses group legend to set categories', () => {
            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
                bar: objectToArray({ a: 4, b: 5, c: 6 }),
            });

            const data = chart.chart.data();
            expect(data).toHaveLength(2);

            expect(data[0].id).toEqual('Foo');
            expect(data[0].values).toHaveLength(3);

            expect(data[1].id).toEqual('Bar');
            expect(data[1].values).toHaveLength(3);
        });

        test('setting new data with missing category removes absent category', () => {
            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
                bar: objectToArray({ a: 4, b: 5, c: 6 }),
            });

            chart.setData({
                foo: objectToArray({ a: 1, b: 2, c: 3 }),
            });

            const data = chart.chart.data();
            expect(data).toHaveLength(1);

            expect(data[0].id).toEqual('Foo');
            expect(data[0].values).toHaveLength(3);
        });
    });
});
