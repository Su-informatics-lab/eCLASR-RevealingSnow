<template>
    <div class="snow-barchart"/>
</template>

<style>
    .snow-barchart {
        display: inline-block;
    }
</style>

<script>
    import * as bb from 'billboard.js';
    import 'billboard.js/dist/billboard.min.css';
    import _ from 'lodash';


    function alignData(data) {
        // Get the list of x-values present across all categories
        const keys = _.uniq(_.flatMap(_.mapValues(data, x => _.map(x, 'name'))));

        // Rebuild the dataset, ensuring that each category has the same set of 'x' values.
        return _.mapValues(data, (category) => {
            const valueLookup = _.keyBy(category, 'name');

            return _.map(keys, (d) => {
                const v = _.get(valueLookup, d, null);

                return {
                    name: d,
                    value: v !== null ? v.value : null,
                };
            });
        });
    }

    export default {
        data() {
            return {
                chart: null,
            };
        },
        props: {
            data: { type: Object, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            title: { type: String, default: '' },
            options: {
                type: Object,
                default() {
                    return {};
                },
            },
            orderFunction: {
                type: Function,
                default: data => _.sortBy(data, d => d.name),
            },
            transformFunction: {
                type: Function,
                default: data => data,
            },
            dataLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
            groupLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
        },
        watch: {
            data(value) {
                this.setData(value);
            },
        },
        mounted() {
            const baseConfig = {
                bindto: this.$el,
                data: {
                    x: 'x',
                    columns: [],
                    type: 'bar',
                },
            };

            const chartConfig = _.defaultsDeep(baseConfig, this.options, {
                size: {
                    width: this.width,
                    height: this.height,
                },
                axis: {
                    x: {
                        type: 'category',
                    },
                },
                legend: {
                    show: false,
                },
                tooltip: {
                    format: {
                        title: this.getTooltipTitle,
                    },
                },
            });

            if (this.title) {
                chartConfig.title = {
                    text: this.title,
                    position: 'top-center',
                };
            }

            this.chart = bb.bb.generate(chartConfig);

            if (this.data) {
                this.setData(this.data);
            }
        },
        methods: {
            setData(value) {
                const aligned = alignData(value);

                _.forIn(aligned, (values, key) => this.setDataGroup(key, values));
            },
            setDataGroup(group, value) {
                const groupLabel = _.get(this.groupLegend, group, group);
                const sorted = this.orderFunction(value);
                const xformed = this.transformFunction(sorted);
                const categories = _.map(xformed, 'name');
                const values = _.map(xformed, 'value');

                this.chart.load({
                    columns: [
                        _.flatten([['x'], categories]),
                        _.flatten([[groupLabel], values]),
                    ],
                });
            },
            getTooltipTitle(index) {
                const key = this.chart.categories()[index];

                if (!_.isEmpty(this.dataLegend)) {
                    return this.dataLegend[key].label;
                }

                return key;
            },
        },
    };
</script>
