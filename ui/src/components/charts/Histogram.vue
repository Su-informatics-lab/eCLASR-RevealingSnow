<template>
    <div class="snow-chart-histogram">
        <bar-chart :stats-key="statsKey"
                   :width="width"
                   :height="height"
                   :options="barChartOptions"
                   :order-function="orderfn"
                   :transform-function="transform"
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
            statsKey: { type: String, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            cumulative: {
                type: Boolean,
                default: false,
            },
        },
        data() {
            return {
                barChartOptions: {
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
                },
            };
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
