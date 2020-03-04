<template>
    <div class="snow-global-demographic-chart">
        <bar-chart :data="data"
                   :width="width"
                   :height="height"
                   :data-legend="legend"
                   :group-legend="demographicLegend"
                   :group-colors="demographicColors"
                   :options="barChartOptions"
                   :title="title"
                   :x-axis-label="xAxisLabel"
                   y-axis-label="# of Patients"
        />
    </div>
</template>

<style scoped>
    .snow-global-demographic-chart {
        display: inline-block;
    }
</style>

<script>
    import _ from 'lodash';
    import BarChart from './BarChart';


    export default {
        name: 'GlobalDemographicChart',
        props: {
            statsKey: { type: String, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            title: { type: String, default: '' },
            xAxisLabel: {
                type: String,
                default: '',
            },
            chartOptions: {
                type: Object,
                default() {
                    return {};
                },
            },
        },
        computed: {
            unfiltered() {
                return this.$store.state.stats.unfiltered[this.statsKey] || [];
            },
            filtered() {
                return this.$store.state.stats.filtered[this.statsKey] || [];
            },
            data() {
                return {
                    filtered: this.filtered,
                    unfiltered: this.unfiltered,
                };
            },
            legend() {
                return this.$store.getters.getLegendObject(this.statsKey);
            },
            demographicLegend() {
                const legend = this.$store.getters.getLegendObject('total');
                return _.mapValues(legend, 'label');
            },
            demographicColors() {
                return this.$store.getters.getLegendColor('total');
            },
            barChartOptions() {
                return _.defaultsDeep(this.chartOptions, {
                    legend: true,
                });
            },
        },
        components: {
            BarChart,
        },
    };
</script>
