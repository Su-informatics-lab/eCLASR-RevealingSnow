<template>
    <div class="snow-report">
        <mode-switch/>

        <report-panel label="Demographics">
            <bar-chart :data="race"
                       width="600"
                       height="300"/>

            <bar-chart :data="sex"
                       width="600"
                       height="300"/>
        </report-panel>

        <report-panel label="Conditions"/>
    </div>
</template>

<style scoped>

</style>

<script>
    import _ from 'lodash';

    import { mapGetters } from 'vuex';
    import ModeSwitch from './ModeSwitch';
    import ReportPanel from './ReportPanel';
    import BarChart from './charts/BarChart';


    function objectToArray(objdata) {
        return _.map(_.keys(objdata), key => ({
            name: key,
            value: objdata[key],
        }));
    }

    export default {
        name: 'Report',
        data() {
            return {
                race: [],
                sex: [],
            };
        },
        components: {
            ModeSwitch,
            ReportPanel,
            BarChart,
        },
        computed: mapGetters(['patientStats']),
        watch: {
            patientStats(result) {
                this.race = objectToArray(result.race);
                this.sex = objectToArray(result.sex);
            },
        },
        mounted() {
            this.$store.dispatch('getPatientStats');
        },
    };
</script>
