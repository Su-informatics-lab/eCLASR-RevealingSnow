<template>
    <div class="snow-filter-panel">
        <div class="snow-condition-filters snow-filter-section">
            <h5>Filters</h5>
            <toggle-filter ref="toggle-filters"
                           v-for="filter in toggleFilters"
                           :key="filter.key"
                           :id="filter.key"
                           :label="filter.label"
                           :default_date="filter.default_date"
            />
        </div>

        <div class="snow-ymca-distance-filters snow-filter-section">
            <h5>YMCA Sites</h5>
            <distance-filter ref="ymca-filters"
                             v-for="site in modelYmcaSites"
                             :key="site.key"
                             :id="site.key"
                             :label="site.label"/>
        </div>

        <button type="submit"
                id="update-filters"
                @click="updateFilters"
                class="btn btn-primary">
            Update
        </button>
    </div>
</template>

<style scoped>
    .snow-filter-panel {
        padding-right: 1em;
        margin-right: 1em;
        border-right: 1px solid lightgrey;
    }

    .snow-filter-section {
        margin-top: 0.5em;
        padding-top: 0.5em;
    }

    #update-filters {
        margin-top: 1em;
    }
</style>

<script>
    import _ from 'lodash';

    import { mapGetters } from 'vuex';
    import ToggleFilter from './filters/ToggleFilter';
    import DistanceFilter from './filters/DistanceFilter';


    function flattenToDotNotation(filters) {
        return _.merge(..._.map(filters, (value, key) => {
            if (typeof value === 'object') {
                return _.mapKeys(value, (subvalue, subkey) => `${key}.${subkey}`);
            }

            return _.fromPairs([[key, value]]);
        }));
    }

    export default {
        name: 'FilterPanel',
        components: {
            ToggleFilter,
            DistanceFilter,
        },
        methods: {
            updateFilters() {
                const filters = flattenToDotNotation(this.filterValues);

                // TODO: Replace with a more graceful way of including distance filters
                const ymcaValue = this.ymcaFilter;
                if (ymcaValue !== null) {
                    filters.ymca_fulton = ymcaValue;
                }

                this.$store.dispatch('getFilteredStats', filters);
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
            ymcaFilter() {
                const ymcaFilter = this.$refs['ymca-filter'];
                return ymcaFilter.value;
            },
        },
        mounted() {
            this.$store.dispatch('getCriteriaDataModel');
        },
    };
</script>
