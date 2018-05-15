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


    export default {
        data() {
            return {
                chart: null,
            };
        },
        props: {
            unfiltered: { type: Array, required: true },
            filtered: { type: Array, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
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
        },
        // computed: {
        //     unfiltered() {
        //         return this.$store.state.stats.unfiltered[this.statsKey];
        //     },
        //     filtered() {
        //         return this.$store.state.stats.filtered[this.statsKey];
        //     },
        // },
        watch: {
            unfiltered(value) {
                this.setData('Unfiltered', value);
            },
            filtered(value) {
                // Align the filtered values to the unfiltered categories; this is only
                // relevant when the filtered is missing some category from the unfiltered,
                // but the results will be misleading if it's not done in that case.
                const valueLookup = _.keyBy(value, 'name');
                const aligned = _.map(this.unfiltered, (d) => {
                    const v = _.get(valueLookup, d.name, null);
                    return {
                        name: d.name,
                        value: v !== null ? v.value : null,
                    };
                });

                this.setData('Filtered', aligned);
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
            });

            this.chart = bb.bb.generate(chartConfig);
        },
        methods: {
            setData(group, value) {
                const sorted = this.orderFunction(value);
                const xformed = this.transformFunction(sorted);
                const categories = _.map(xformed, 'name');
                const values = _.map(xformed, 'value');

                this.chart.load({
                    columns: [
                        _.flatten([['x'], categories]),
                        _.flatten([[group], values]),
                    ],
                });
            },
        },
    };
</script>
