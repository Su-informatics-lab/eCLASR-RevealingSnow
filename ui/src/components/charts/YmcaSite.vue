<template>
    <div class="snow-chart-ymca-site">
        <histogram :unfiltered="unfiltered"
                   :filtered="filtered"
                   :width="width"
                   :height="height"
                   :cumulative="true"
                   :title="label"/>
    </div>
</template>

<style scoped>
    .snow-chart-ymca-site {
        display: inline-block;
    }
</style>

<script>
    import _ from 'lodash';

    import Histogram from './Histogram';


    function objectToArray(objdata) {
        return _.map(_.keys(objdata), key => ({
            name: key,
            value: objdata[key],
        }));
    }

    export default {
        name: 'YmcaSite',
        props: {
            id: {
                type: String,
                required: true,
            },
            width: { type: Number, required: true },
            height: { type: Number, required: true },
        },
        data() {
            return {
                unfiltered: [],
                filtered: [],
            };
        },
        computed: {
            cutoff() {
                return this.$store.state.filters.ymcaSites[this.id].cutoff;
            },
            filters() {
                return this.$store.state.filters.criteria;
            },
            label() {
                return this.$store.getters.ymcaSiteByKey(this.id).label;
            },
        },
        watch: {
            cutoff() {
                this.reloadData();
            },
            filters() {
                this.loadFiltered();
            },
        },
        mounted() {
            this.reloadData();
        },
        methods: {
            reloadData() {
                this.loadUnfiltered();

                if (this.filters) {
                    this.loadFiltered();
                }
            },
            loadUnfiltered() {
                this.$api.getYmcaStats(this.id, this.cutoff).then((result) => {
                    this.unfiltered = objectToArray(result[this.id]);
                });
            },
            loadFiltered() {
                this.$api.getYmcaStats(this.id, this.cutoff, this.filters).then((result) => {
                    this.filtered = objectToArray(result[this.id]);
                });
            },
        },
        components: {
            Histogram,
        },
    };
</script>
