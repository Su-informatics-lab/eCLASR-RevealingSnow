<template>
    <div class="snow-report">
        <report-panel label="Demographics">
            <bar-chart stats-key="race"
                       :width="300"
                       :height="200"/>

            <bar-chart stats-key="sex"
                       :width="300"
                       :height="200"/>

            <bar-chart stats-key="ethnicity"
                       :width="300"
                       :height="200"/>

            <histogram stats-key="age"
                       :width="900"
                       :height="200"/>
        </report-panel>

        <report-panel label="Conditions">
            Placeholder
        </report-panel>

        <report-panel label="YMCA Proximity">
            Placeholder
        </report-panel>
    </div>
</template>

<style scoped>

</style>

<script>
    import ReportPanel from './ReportPanel';
    import BarChart from './charts/BarChart';
    import Histogram from './charts/Histogram';


    export default {
        name: 'Report',
        components: {
            ReportPanel,
            BarChart,
            Histogram,
        },
        mounted() {
            this.$store.dispatch('getFilteredStats');
        },
    };
</script>
