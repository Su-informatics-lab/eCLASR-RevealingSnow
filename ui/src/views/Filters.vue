<template>
    <div class="snow-filter-panel">
        <metadata-uploader ref="uploader"
                           @metadata-uploaded="updateControlsFromMetadata"/>

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
                    <!-- TODO: Fix layout -->
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="resetAll">Reset</a>
                    </li>
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="deselectAll">None</a>
                    </li>
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="uploadMetadata">
                            <font-awesome-icon icon="cloud-upload-alt"/>
                        </a>
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
                           :default_value="getFilterValue(filter)"
                           :description="filter.description"
            />

            <select-filter id="pt_status"
                           label="Recruitment Status"
                           :enabled="false"/>

            <range-filter ref="range-filters"
                          @updated="updateFilters"
                          v-for="filter in rangeFilters"
                          :key="filter.key"
                          :id="filter.key"
                          :label="filter.label"
                          :description="filter.description"
                          :min-value="filter.minimum_value"
                          :max-value="filter.maximum_value"
            />

            <limit-filter ref="limit-filter"
                          @updated="updateLimits"
                          id="limit"
                          label="Limit Results"/>
        </div>

        <div class="snow-ymca-distance-filters snow-filter-section">
            <div class="snow-filter-header">
                <h5>YMCA Sites</h5>

                <ul class="snow-condition-filter-bulk-controls">
                    <li class="bulk-control">
                        <a tabindex="0"
                           @click="clearYmcaSites">Clear</a>
                    </li>
                </ul>
            </div>

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
        padding-right: 0.5em;
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
    import SelectFilter from '../components/filters/SelectFilter';
    import LimitFilter from '../components/filters/LimitFilter';
    import RangeFilter from '../components/filters/RangeFilter';
    import MetadataUploader from '../components/MetadataUploader';


    const DEBOUNCE_DELAY = 500;

    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
            DistanceFilter,
            FontAwesomeIcon,
            SelectFilter,
            LimitFilter,
            RangeFilter,
            MetadataUploader,
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
                this.$store.dispatch('setActiveFilters', { criteria: this.filterValues, sites: this.ymcaSites });
            }, DEBOUNCE_DELAY),

            // eslint-disable-next-line func-names
            updateSites: _.debounce(function () {
                this.$store.dispatch('setActiveSites', { sites: this.ymcaSites });
            }, DEBOUNCE_DELAY),

            updateLimits: _.debounce(function () {
                this.$store.dispatch('setResultLimits', { limits: this.resultLimits });
            }, DEBOUNCE_DELAY),

            selectAll() {
                _.each(this.$refs['toggle-filters'], f => f.setSelected(false));
            },
            deselectAll() {
                _.each(this.$refs['toggle-filters'], f => f.setSelected(null));
            },
            resetAll() {
                _.each(this.$refs['toggle-filters'], f => f.resetToDefault());
                _.each(this.$refs['range-filters'], f => f.resetToDefault());
            },
            clearYmcaSites() {
                _.each(this.$refs['ymca-sites'], f => f.setSelected(false));
            },
            uploadMetadata() {
                this.$refs.uploader.showDialog();
            },
            updateControlsFromMetadata(filters) {
                this.updateFiltersFromMetadata(filters.criteria);
                this.updateSitesFromMetadata(filters.sites);
                this.updateLimitsFromMetadata(filters.limits);
            },
            updateFiltersFromMetadata(criteria) {
                this.updateToggleFiltersFromMetadata(criteria);
                this.updateRangeFiltersFromMetadata(criteria);
            },
            updateToggleFiltersFromMetadata(criteria) {
                _.each(this.$refs['toggle-filters'], (f) => {
                    if (_.has(criteria, f.id)) {
                        f.set(criteria[f.id]);
                    } else {
                        // If the criterion is missing, then it's excluded
                        f.setSelected(null);
                    }
                });
            },
            updateRangeFiltersFromMetadata(criteria) {
                _.each(this.$refs['range-filters'], (f) => {
                    if (_.has(criteria, f.id)) {
                        f.set(criteria[f.id]);
                    } else {
                        // If the criterion is missing, then it's excluded
                        f.setEnabled(false);
                    }
                });
            },
            updateSitesFromMetadata(sites) {
                _.each(this.$refs['ymca-sites'], (f) => {
                    if (_.has(sites, f.id)) {
                        f.setSelected(true);
                        f.setMaxdist(sites[f.id].maxdist);
                        f.setMindist(sites[f.id].mindist);
                    } else {
                        // If the criterion is missing, then it's excluded
                        f.setSelected(false);
                    }
                });
            },
            updateLimitsFromMetadata(limits) {
                const filter = this.$refs['limit-filter'];

                if (limits) {
                    filter.setEnabled(true);
                    filter.setLimit(limits.limit);
                    filter.setOrderColumn(limits.order_by);
                    filter.setOrderAscending(limits.order_asc);
                } else {
                    filter.setEnabled(false);
                }
            },
            getFilterValue(filter) {
                return _.get(filter, 'default_value', false);
            },
        },
        computed: {
            ...mapGetters(['modelFilters', 'modelYmcaSites']),
            toggleFilters() {
                return _.filter(this.modelFilters, o => o.type === 'toggle');
            },
            rangeFilters() {
                return _.filter(this.modelFilters, o => o.type === 'range');
            },
            filterValues() {
                return _.merge({}, this.rangeFilterValues, this.toggleFilterValues);
            },
            rangeFilterValues() {
                const activeFilters = _.keyBy(_.filter(this.$refs['range-filters'], f => f.enabled), 'id');
                return _.mapValues(activeFilters, f => f.value);
            },
            toggleFilterValues() {
                const activeFilters = _.keyBy(_.filter(this.$refs['toggle-filters'], f => f.checked), 'id');
                return _.mapValues(activeFilters, f => f.value);
            },
            ymcaSites() {
                const activeSites = _.keyBy(_.filter(this.$refs['ymca-sites'], f => f.enabled), 'id');
                return _.mapValues(activeSites, f => f.value);
            },
            resultLimits() {
                const limitFilter = this.$refs['limit-filter'];
                if (!limitFilter.enabled) {
                    return null;
                }

                return limitFilter.value;
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
