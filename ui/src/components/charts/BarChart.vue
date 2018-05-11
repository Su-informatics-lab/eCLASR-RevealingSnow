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
            data: { type: Array, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            options: {
                type: Object,
                default() {
                    return {};
                },
            },
        },
        watch: {
            data(value) {
                const sorted = _.sortBy(value, d => d.name);
                const categories = _.map(sorted, 'name');
                const values = _.map(sorted, 'value');
                // const values = _.map(_.map(value, 'value'), () => _.random(0, 500));

                this.chart.load({
                    columns: [
                        _.flatten([['x'], categories]),
                        _.flatten([['y'], values]),
                    ],
                });
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
    };
</script>
