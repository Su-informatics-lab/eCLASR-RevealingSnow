<template>
    <div class="row">
        <filters class="col-2"/>
        <div class="col">

            <bar-chart :data="race"
                       width="600"
                       height="300"/>

            <bar-chart :data="sex"
                       width="600"
                       height="300"/>
        </div>
    </div>
</template>

<style>
</style>

<script>
    import _ from 'lodash';
    import { mapGetters } from 'vuex';

    import Filters from './Filters';
    import BarChart from './charts/BarChart';


    function objectToArray(objdata) {
        return _.map(_.keys(objdata), key => ({
            name: key,
            value: objdata[key],
        }));
    }

    export default {
        data() {
            return {
                race: [],
                sex: [],
            };
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
        components: {
            BarChart,
            Filters,
        },
    };
</script>
