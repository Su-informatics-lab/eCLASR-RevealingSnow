<template>
    <div class="snow-filter-panel">
        <div class="snow-condition-filters snow-filter-section">
            <div class="snow-filter-header">
                <h5>
                    Filters

                    <a ref="legend-link"
                       tabindex="0"
                       role="button"
                       class="snow-filter-legend"
                       data-trigger="focus"
                       data-toggle="popover"
                       v-if="description"
                       data-popover-content="#filter-description">
                        <sup>?</sup>
                    </a>
                </h5>

                <div class="hidden"
                     id="filter-description">
                    <ul class="legend-list">
                        <li>
                            <font-awesome-icon icon="circle-notch"/>
                            Do not incorporate this condition when selecting patients.
                        </li>
                        <li>
                            <font-awesome-icon icon="plus-circle"/>
                            Only include patients with this condition on or after the
                            specified date.
                        </li>
                        <li>
                            <font-awesome-icon icon="times-circle"/>
                            Exclude patients with this condition on or after the specified date.
                        </li>
                    </ul>
                </div>


                <ul class="snow-condition-filter-bulk-controls">
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="selectAll">All</a>
                    </li>
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="deselectAll">None</a>
                    </li>
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="resetAll">Reset</a>
                    </li>
                </ul>
            </div>

            <toggle-filter ref="toggle-filters"
                           @updated="updateFilters"
                           v-for="filter in toggleFilters"
                           :key="filter.key"
                           :id="filter.key"
                           :label="filter.label"
                           :default_date="filter.default_date"
                           :default_value="false"
                           :description="filter.description"
            />
        </div>

        <div class="snow-ymca-distance-filters snow-filter-section">
            <h5>YMCA Sites</h5>

            <div class="snow-distance-filters">
                <distance-filter ref="ymca-sites"
                                 @updated="updateSites"
                                 v-for="site in modelYmcaSites"
                                 :key="site.key"
                                 :id="site.key"
                                 :label="site.label"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .snow-filter-panel {
        /*padding-right: 1em;*/
        /*margin-right: 1em;*/
        padding-bottom: 1em;

        border-right: 1px solid #999;
        background: #EEEBE0;
    }

    .snow-filter-section {
        margin-top: 0.5em;
        padding-top: 0.5em;
    }

    .snow-filter-header > h5 {
        display: inline-block;
    }

    .snow-condition-filter-bulk-controls {
        display: inline-block;
        list-style: none;

        font-size: smaller;
    }

    .snow-condition-filter-bulk-controls a {
        cursor: pointer;
    }

    .snow-distance-filters {
        padding-left: 0.5em;
    }

    .bulk-control {
        display: inline-block;
    }

    .bulk-control + .bulk-control {
        padding-left: 0.25em;
    }

    .bulk-control + .bulk-control::before {
        display: inline-block;
        content: "|";
        padding-right: 0.25em;
    }

    .snow-filter-legend {
        font-size: xx-small;
        font-weight: bold;
        cursor: pointer;
    }

    .legend-list {
        margin: 0;
        padding: 0;

        list-style-type: none;
    }

    .hidden {
        display: none;
    }

    svg[data-icon="times-circle"] {
        color: red;
    }

    svg[data-icon="plus-circle"] {
        color: green;
    }
</style>

<script>
    import $ from 'jquery';

    import _ from 'lodash';
    import Vue from 'vue';

    import FontAwesomeIcon from '@fortawesome/vue-fontawesome';

    import { mapGetters } from 'vuex';
    import ToggleFilter from '../components/filters/ToggleFilter';
    import DistanceFilter from '../components/filters/DistanceFilter';


    function flattenToDotNotation(filters) {
        return _.merge(..._.map(filters, (value, key) => {
            if (typeof value === 'object') {
                return _.mapKeys(value, (subvalue, subkey) => `${key}.${subkey}`);
            }

            return _.fromPairs([[key, value]]);
        }));
    }

    const DEBOUNCE_DELAY = 500;

    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
            DistanceFilter,
            FontAwesomeIcon,
        },
        data() {
            return {
                description: true,
                ready: false,
            };
        },
        methods: {
            // eslint-disable-next-line func-names
            updateFilters: _.debounce(function () {
                const criteria = flattenToDotNotation(this.filterValues);
                this.$store.dispatch('setActiveFilters', { criteria, sites: this.ymcaSites });
            }, DEBOUNCE_DELAY),
            updateSites: _.debounce(function () {
                this.$store.dispatch('setActiveSites', { sites: this.ymcaSites });
            }, DEBOUNCE_DELAY),
            selectAll() {
                _.each(this.$refs['toggle-filters'], f => f.setSelected(false));
            },
            deselectAll() {
                _.each(this.$refs['toggle-filters'], f => f.setSelected(null));
            },
            resetAll() {
                _.each(this.$refs['toggle-filters'], f => f.resetToDefault());
            },
        },
        computed: {
            ...mapGetters(['modelFilters', 'modelYmcaSites']),
            toggleFilters() {
                return _.filter(this.modelFilters, o => o.type === 'toggle');
            },
            filterValues() {
                const activeFilters = _.keyBy(_.filter(this.$refs['toggle-filters'], f => f.checked), 'id');
                return _.mapValues(activeFilters, f => f.value);
            },
            ymcaSites() {
                const activeSites = _.keyBy(_.filter(this.$refs['ymca-sites'], f => f.enabled), 'id');
                return _.mapValues(activeSites, f => f.value);
            },
        },
        mounted() {
            this.$store.dispatch('getCriteriaDataModel');

            // Initialize the legend popover
            $(this.$refs['legend-link']).popover({
                html: true,
                content() {
                    const content = $(this).attr('data-popover-content');
                    return $(content).html();
                },
            });
        },
        watch: {
            toggleFilters() {
                // Wait until all of the toggle controls have been built before
                // initial update.
                Vue.nextTick(() => {
                    this.ready = true;
                    this.updateFilters();
                });
            },
        },
    };
</script>
