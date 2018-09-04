<template>
    <div class="snow-chart-histogram">
        <bar-chart :data="data"
                   :width="width"
                   :height="height"
                   :max-width="width * 2"
                   :max-height="height * 2"
                   :allow-resize="allowResize"
                   :options="barChartOptions"
                   :order-function="orderfn"
                   :transform-function="transform"
                   :title="title"
                   :group-legend="groupLegend"
                   @resized="$emit('resized')"
        />
    </div>
</template>

<style scoped>

</style>

<script>
    import _ from 'lodash';

    import BarChart from './BarChart';


    export default {
        name: 'Histogram',
        props: {
            data: { type: Object, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            allowResize: { type: Boolean, default: false },
            title: { type: String, default: '' },
            cumulative: {
                type: Boolean,
                default: false,
            },
            groupLegend: {
                type: Object,
                default() {
                    return {};
                },
            },
            chartOptions: {
                type: Object,
                default() {
                    return {};
                },
            },
        },
        computed: {
            barChartOptions() {
                return _.defaultsDeep(this.chartOptions, {
                    axis: {
                        x: {
                            tick: {
                                culling: {
                                    max: 10,
                                },
                                format: (idx, name) => _.round(name),
                            },
                        },
                    },
                });
            },
        },
        components: {
            BarChart,
        },
        methods: {
            orderfn(data) {
                return _.sortBy(data, d => _.round(d.name));
            },
            transform(data) {
                if (this.cumulative) {
                    return this.cumsum(data);
                }

                return data;
            },
            cumsum(data) {
                // Adapted from https://stackoverflow.com/a/11891025/228591
                return _.reduce(data, (acc, x) => {
                    const value = (acc.length > 0 ? acc[acc.length - 1].value : 0) + x.value;

                    acc.push({
                        name: x.name,
                        value,
                    });

                    return acc;
                }, []);
            },
        },
    };
</script>
