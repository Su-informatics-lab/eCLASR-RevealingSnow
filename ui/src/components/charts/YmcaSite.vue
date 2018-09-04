<template>
    <div class="snow-chart-ymca-site">
        <isotope :list="demographicKeys"
                 :options="isotopeOptions"
                 ref="isotope-grid">
            <div v-for="key in demographicKeys"
                 :key="key">
                <demographic-histogram :data="demographics"
                                       :demographic="key"
                                       :width="width"
                                       :height="height"
                                       :cumulative="true"
                                       :title="key"
                                       :allow-resize="true"
                                       @resized="layout"
                />
            </div>
        </isotope>
    </div>
</template>

<style scoped>
    .snow-chart-ymca-site {
    }
</style>

<script>
    import _ from 'lodash';
    import isotope from 'vueisotope';

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
                demographics: {},
                isotopeOptions: {
                    layoutMode: 'fitRows',
                },
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
            demographicKeys() {
                if (!_.isEmpty(this.demographics)) {
                    // The 'total' key always comes first
                    return _.concat(['total'], _.without(_.keys(this.demographics), 'total'));
                }

                return [];
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
                    this.demographics.total = {
                        filtered: objectToArray(this.filtered),
                        unfiltered: objectToArray(this.unfiltered),
                    };
                });
            },
            orderfn(data) {
                return _.sortBy(data, d => _.round(d.name));
            },
            layout() {
                this.$refs['isotope-grid'].layout();
            },
        },
        components: {
            Histogram,
            BarChart,
            DemographicHistogram,
            isotope,
        },
    };
</script>
