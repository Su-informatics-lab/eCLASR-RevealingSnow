<template>
    <div class="snow-chart-ymca-site">
        <div class="ymca-site-header"
             @click="toggleBody">
            {{ label }}

            <font-awesome-icon class="ymca-site-header-expansion-icon"
                               :icon="expansionIcon"/>
        </div>

        <div class="ymca-site-body"
             :class="{ 'hidden': !expanded }">
            <isotope :list="demographicKeys"
                     :options="isotopeOptions"
                     ref="isotope-grid">
                <div class="ymca-site-chart"
                     v-for="key in demographicKeys"
                     :key="key">
                    <demographic-histogram :data="demographics"
                                           :demographic="key"
                                           :width="width"
                                           :height="height"
                                           :cumulative="true"
                                           :title="key"
                                           :allow-resize="true"
                                           :percent-by-group="false"
                                           @resized="layout"
                    />
                </div>
            </isotope>
        </div>

    </div>
</template>

<style scoped>
    .snow-chart-ymca-site {
        border: 1px solid #ddd;
        border-radius: 5px;

        margin: 0.5em;
    }

    .ymca-site-header {
        position: relative;

        background: #FAF7EC;
        font-weight: bold;
        font-size: larger;

        border-radius: 5px;
        padding: 0.5em;

        cursor: pointer;
    }

    .ymca-site-header-expansion-icon {
        position: absolute;
        top: 0;
        right: 1em;
        height: 100%;
    }

    .ymca-site-body {
        padding: 0.5em;
    }

    .hidden {
        display: none;
    }

    .ymca-site-chart {
        padding: 0.5em;
    }
</style>

<script>
    import _ from 'lodash';
    import isotope from 'vueisotope';
    import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
    import { faChevronDown, faChevronRight } from '@fortawesome/fontawesome-free-solid';
    import Vue from 'vue';

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
                expanded: true,
                isotopeOptions: {
                    layoutMode: 'fitRows',
                },
            };
        },
        computed: {
            maxdist() {
                return this.$store.state.filters.ymcaSites[this.id].maxdist;
            },
            mindist() {
                return this.$store.state.filters.ymcaSites[this.id].mindist;
            },
            filters() {
                return this.$store.state.filters.criteria;
            },
            limits() {
                return this.$store.state.filters.limits;
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
            expansionIcon() {
                return this.expanded ? faChevronDown : faChevronRight;
            },
        },
        watch: {
            maxdist() {
                this.reloadData();
            },
            mindist() {
                this.reloadData();
            },
            filters() {
                this.loadFiltered();
            },
            limits() {
                this.reloadData();
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
                this.$api.getYmcaStats(this.id, this.maxdist, this.mindist).then((result) => {
                    this.unfiltered = _.pick(result[this.id], 'total').total;
                });
            },
            loadFiltered() {
                const { id, mindist, maxdist, filters } = this;
                this.$api.getYmcaStats(id, maxdist, mindist, filters).then((result) => {
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
                Vue.nextTick(() => {
                    this.$refs['isotope-grid'].layout();
                });
            },
            toggleBody() {
                this.expanded = !this.expanded;

                if (this.expanded) {
                    this.layout();
                }
            },
        },
        components: {
            Histogram,
            BarChart,
            DemographicHistogram,
            isotope,
            FontAwesomeIcon,
        },
    };
</script>
