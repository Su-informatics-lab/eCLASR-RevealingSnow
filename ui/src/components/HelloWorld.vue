<template>
    <div class="hello-dc">
        <bar-chart :data="race"
                   width="600"
                   height="300"/>

        <bar-chart :data="sex"
                   width="600"
                   height="300"/>
    </div>
</template>

<style>
</style>

<script>
    import _ from 'lodash';
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
        mounted() {
            this.$api.getPatientStats(null).then((result) => {
                this.race = objectToArray(result.race);
                this.sex = objectToArray(result.sex);
            });
        },
        components: {
            BarChart,
        },
    };
</script>
