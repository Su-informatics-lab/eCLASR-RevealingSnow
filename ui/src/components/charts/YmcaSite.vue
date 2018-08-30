<template>
    <div class="snow-chart-ymca-site">
        <histogram :data="totalData"
                   :width="width"
                   :height="height"
                   :cumulative="true"
                   :title="label"
                   :group-legend="{filtered: 'Filtered', unfiltered: 'Unfiltered'}"/>

        <demographic-histogram :data="demographics"
                               demographic="race"
                               :width="width"
                               :height="height"
                               :cumulative="true"/>

        <demographic-histogram :data="demographics"
                               demographic="sex"
                               :width="width"
                               :height="height"
                               :cumulative="true"/>

        <demographic-histogram :data="demographics"
                               demographic="ethnicity"
                               :width="width"
                               :height="height"
                               :cumulative="true"/>
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
    import BarChart from './BarChart';
    import DemographicHistogram from './DemographicHistogram';


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
                filteredStats: [],
                unfilteredStats: [],
                data: {},
                rd: {},
                totals: {},
                demographics: {},
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
            totalData() {
                return {
                    filtered: objectToArray(this.filtered),
                    unfiltered: objectToArray(this.unfiltered),
                };
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
                    this.unfiltered = _.pick(result[this.id], 'total').total;
                });
            },
            loadFiltered() {
                this.$api.getYmcaStats(this.id, this.cutoff, this.filters).then((result) => {
                    this.filtered = _.pick(result[this.id], 'total').total;
                    this.demographics = _.mapValues(
                        _.omit(result[this.id], 'total'),
                        x => _.mapValues(x, objectToArray),
                    );
                });
            },
            orderfn(data) {
                return _.sortBy(data, d => _.round(d.name));
            },
        },
        components: {
            Histogram,
            BarChart,
            DemographicHistogram,
        },
    };
</script>
