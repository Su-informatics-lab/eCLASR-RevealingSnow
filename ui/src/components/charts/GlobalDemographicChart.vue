<template>
    <div class="snow-global-demographic-chart">
        <bar-chart :unfiltered="unfiltered"
                   :filtered="filtered"
                   :width="width"
                   :height="height"/>
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
        },
        computed: {
            unfiltered() {
                return this.$store.state.stats.unfiltered[this.statsKey];
            },
            filtered() {
                return this.$store.state.stats.filtered[this.statsKey];
            },
        },
        components: {
            BarChart,
        },
    };
</script>
