<template>
    <div class="snow-global-demographic-chart">
        <bar-chart :data="data"
                   :width="width"
                   :height="height"
                   :data-legend="legend"
                   :group-legend="{filtered: 'Filtered', unfiltered: 'Unfiltered'}"
                   :title="title"
        />
    </div>
</template>

<style scoped>
    .snow-global-demographic-chart {
        display: inline-block;
    }
</style>

<script>
    import BarChart from './BarChart';


    export default {
        name: 'GlobalDemographicChart',
        props: {
            statsKey: { type: String, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
            title: { type: String, default: '' },
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
        },
        components: {
            BarChart,
        },
    };
</script>
