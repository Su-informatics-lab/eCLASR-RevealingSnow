<template>
    <div class="snow-global-demographic-chart">
        <bar-chart :data="data"
                   :width="width"
                   :height="height"
                   :data-legend="legend"
                   :group-legend="{filtered: 'Eligible', unfiltered: 'Overall'}"
                   :options="barChartOptions"
                   :title="title"
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
                    unfiltered: this.unfiltered,
                    filtered: this.filtered,
                };
            },
            legend() {
                return this.$store.getters.getLegendObject(this.statsKey);
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
