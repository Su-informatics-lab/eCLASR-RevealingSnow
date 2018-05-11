<template>
    <div class="snow-report">
        <mode-switch/>

        <report-panel label="Demographics">
            <bar-chart :data="race"
                       :width="300"
                       :height="200"/>

            <bar-chart :data="sex"
                       :width="300"
                       :height="200"/>

            <bar-chart :data="ethnicity"
                       :width="300"
                       :height="200"/>

            <histogram :data="age"
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
    import _ from 'lodash';

    import { mapGetters } from 'vuex';
    import ModeSwitch from './ModeSwitch';
    import ReportPanel from './ReportPanel';
    import BarChart from './charts/BarChart';
    import Histogram from './charts/Histogram';


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
                ethnicity: [],
                age: [],
            };
        },
        components: {
            ModeSwitch,
            ReportPanel,
            BarChart,
            Histogram,
        },
        computed: mapGetters(['patientStats']),
        watch: {
            patientStats(result) {
                this.race = objectToArray(result.race);
                this.sex = objectToArray(result.sex);
                this.ethnicity = objectToArray(result.ethnicity);
                this.age = objectToArray(result.age);
            },
        },
        mounted() {
            this.$store.dispatch('getPatientStats');
        },
    };
</script>
