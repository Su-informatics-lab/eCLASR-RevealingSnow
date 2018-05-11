<template>
    <div class="snow-chart-histogram">
        <bar-chart :stats-key="statsKey"
                   :width="width"
                   :height="height"
                   :options="barChartOptions"
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
        },
        data() {
            return {
                barChartOptions: {
                    axis: {
                        x: {
                            tick: {
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
    };
</script>
